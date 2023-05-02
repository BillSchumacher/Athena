from itertools import islice
from typing import Any
from datetime import datetime
from cityhash import CityHash64
from athena.crud.response import create_response
from athena.db import get_db, session_scope
from athena.memory.redis import redis_client
from athena.memory.redis_vector import add_text_embedding, create_index, search_similar
import numpy as np
import openai
import tiktoken
from tenacity import (
    retry,
    retry_if_not_exception_type,
    stop_after_attempt,
    wait_random_exponential,
)
from loguru import logger

from athena.models.api import Response


EMBEDDING_MODEL = "text-embedding-ada-002"
EMBEDDING_CTX_LENGTH = 8191
EMBEDDING_ENCODING = "cl100k_base"


def batched(iterable, n):
    """Batch data into tuples of length n. The last batch may be shorter."""
    # batched('ABCDEFG', 3) --> ABC DEF G
    if n < 1:
        raise ValueError("n must be at least one")
    it = iter(iterable)
    while batch := tuple(islice(it, n)):
        yield batch


def chunked_tokens(text, encoding_name, chunk_length):
    encoding = tiktoken.get_encoding(encoding_name)
    tokens = encoding.encode(text)
    yield from batched(tokens, chunk_length)


def len_safe_get_embedding(
    text,
    model=EMBEDDING_MODEL,
    max_tokens=EMBEDDING_CTX_LENGTH,
    encoding_name=EMBEDDING_ENCODING,
    average=True,
    hashed_key=None,
):
    chunk_embeddings = []
    chunk_lens = []
    for chunk in chunked_tokens(
        text, encoding_name=encoding_name, chunk_length=max_tokens
    ):
        chunk_embeddings.append(get_embedding(chunk, model=model, hashed_key=hashed_key))
        chunk_lens.append(len(chunk))
    averaged_embeddings = []
    if average:
        averaged_embeddings = np.average(chunk_embeddings, axis=0, weights=chunk_lens)
        # normalizes length to 1
        averaged_embeddings = averaged_embeddings / np.linalg.norm(averaged_embeddings)
        averaged_embeddings = averaged_embeddings.tolist()
        logger.debug(f"averaged_embeddings: {averaged_embeddings}")
        if hashed_key:
            try:
                create_index(f"{model}:average")
            except Exception as e:
                logger.debug(e)
            try:
                add_text_embedding(
                    index_name=f"{model}:average",
                    key=hashed_key,
                    text=text,
                    embedding=convert_embeddings_to_np(averaged_embeddings).tobytes()
                )
                redis_client.sadd(hashed_key, f"{model}:average:{hashed_key}")
            except Exception as e:
                logger.error(e)
    return chunk_embeddings, averaged_embeddings


# let's make sure to not retry on an invalid request,
# because that is what we want to avoid
@retry(
    wait=wait_random_exponential(min=1, max=20),
    stop=stop_after_attempt(2),
    retry=retry_if_not_exception_type(openai.InvalidRequestError),
)
def get_embedding(text_or_tokens, model=EMBEDDING_MODEL, hashed_key=None):
    result = openai.Embedding.create(input=text_or_tokens, model=model)
    logger.debug(f"Embedding result: {result}")
    with session_scope() as session:
        response_obj = Response(
            created=datetime.now(),
            model=result['model'],
            object_type=result['object'],
            usage_prompt_tokens=result['usage']['prompt_tokens']
        )
        response = create_response(session, response_obj)
        response_id = response.id
    embedding = result["data"][0]["embedding"]
    try:
        create_index(result['model'])
    except Exception as e:
        logger.debug(e)
    try:
        add_text_embedding(
            index_name=result['model'],
            key=response_id,
            text=text_or_tokens,
            embedding=convert_embeddings_to_np(embedding).tobytes()
        )
        if hashed_key:
            redis_client.sadd(hashed_key, f"{result['model']}:{response_id}")
    except Exception as e:
        logger.error(e)
    return embedding


def get_openai_embedding(
    text: str,
    model: str = EMBEDDING_MODEL,
    embedding_encoding: str = EMBEDDING_ENCODING,
    max_tokens: int = EMBEDDING_CTX_LENGTH,
):
    """Returns the OpenAI embedding for the given text.

    Args:
        text (str): The text for which the embedding is to be generated.
        model (str): The name of the model to use for generating the embedding.
        encoding (str): The name of the encoding to use for generating the embedding.
    Returns:
        list: The embedding for the given text.
    """
    text_hash = CityHash64(text)
    logger.debug(f"Getting embedding for {text_hash}")
    logger.debug(f"Text: {text}")
    if embedding_keys := redis_client.smembers(text_hash):
        return get_cached_embeddings(embedding_keys, text_hash)
    encoding = tiktoken.get_encoding(embedding_encoding)
    tokens = encoding.encode(text)
    token_length = len(tokens)
    logger.debug(f"Token length: {token_length}")
    if token_length > max_tokens:
        logger.debug(f"Token length > max tokens: {token_length} > {max_tokens}")
        logger.debug("Splitting text into chunks")
        return len_safe_get_embedding(
            text, model=model, max_tokens=max_tokens, encoding_name=embedding_encoding,
            hashed_key=text_hash
        )
    logger.debug("Getting embedding from OpenAI")
    return [get_embedding(text, model, hashed_key=text_hash)], []


def get_cached_embeddings(embedding_keys, text_hash):
    averaged = []
    embeddings = []
    pipe = redis_client.pipeline()
    for key in embedding_keys:
        average_key = f"{text_hash}:{key}:average"
        pipe.hgetall(key)
        pipe.hgetall(average_key)
    results = pipe.execute()
    for i in range(0, len(results), 2):
        embeddings.append(results[i])
        averaged.append(results[i + 1])
    return embeddings, averaged


def convert_embeddings_to_np(embeddings) -> np.ndarray[Any, np.dtype[np.float32]]:
    return np.array(embeddings).astype(np.float32)


# Split a text into smaller chunks of size n, preferably ending at the end of a sentence
def create_chunks(text, n, tokenizer):
    tokens = tokenizer.encode(text)
    """Yield successive n-sized chunks from text."""
    i = 0
    while i < len(tokens):
        # Find the nearest end of sentence within a range of 0.5 * n and 1.5 * n tokens
        j = min(i + int(1.5 * n), len(tokens))
        while j > i + int(0.5 * n):
            # Decode the tokens and check for full stop or newline
            chunk = tokenizer.decode(tokens[i:j])
            if chunk.endswith(".") or chunk.endswith("\n"):
                break
            j -= 1
        # If no end of sentence found, use n tokens as the chunk size
        if j == i + int(0.5 * n):
            j = min(i + n, len(tokens))
        yield tokens[i:j]
        i = j
