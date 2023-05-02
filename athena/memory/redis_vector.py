from __future__ import annotations

import time
from typing import Optional

from loguru import logger
from redis.commands.search.field import NumericField, TextField, VectorField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import Query
from redis.commands.search.result import Result

from athena.memory.redis import redis_client

SCHEMA = [
    TextField("data"),
    NumericField("timestamp"),
    NumericField("response_id"),
    VectorField(
        "embedding",
        "HNSW",
        {"TYPE": "FLOAT32", "DIM": 1536, "DISTANCE_METRIC": "COSINE"},
    ),
]


def create_index(index_name: str) -> bool:
    """
    Creates a Redis search index.

    Args:
        index_name: The name of the index to create.

    Returns: True if the index was created successfully, False otherwise.
    """
    try:
        redis_client.ft(index_name).create_index(
            fields=SCHEMA,
            definition=IndexDefinition(
                prefix=[f"{index_name}:"], index_type=IndexType.HASH
            ),
        )
        return True
    except Exception as e:
        logger.error("Error creating Redis search index: ", e)
        return False


def add_text_embedding(index_name: str, key: int, text: str, embedding: bytes) -> None:
    """
    Adds a text and its embedding to the Redis search index.

    Args:
        index_name: The name of the index to add the text and embedding to.
        text: The text to add.
        embedding: The embedding to add.
    """
    data_dict = {
        b"data": text,
        "timestamp": time.time(),
        "response_id": key,
        "embedding": embedding,
    }
    redis_client.hset(f"{index_name}:{key}", mapping=data_dict)


def search_similar(
    index_name: str, embedding: bytes, num_results: int = 5
) -> Optional[Result]:
    """
    Searches the Redis search index for similar embeddings.

    Args:
        index_name: The name of the index to search.
        embedding: The embedding to search for.
        num_results: The number of results to return.

    Returns: A list of the most similar embeddings.
    """
    base_query = f"*=>[KNN {num_results} @embedding $vector AS vector_score]"
    query = (
        Query(base_query)
        .return_fields("data", "vector_score")
        .sort_by("vector_score")
        .dialect(2)
    )

    try:
        return redis_client.ft(f"{index_name}").search(
            query, query_params={"vector": embedding}
        )
    except Exception as e:
        logger.error("Error calling Redis search: %s", str(e))
        return None


def get_stats(index_name: str) -> dict:
    """
    Gets the stats for the given memory index.

    Args:
        index_name: The name of the index to get the stats for.

    Returns: The stats of the memory index.
    """
    return redis_client.ft(index_name).info()
