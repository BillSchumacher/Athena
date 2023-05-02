import os

import openai
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_random_exponential

from athena.llm.openai.embedding import get_openai_embedding


def openai_completion_cache_key(**kwargs):
    pass


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def completion_with_backoff(**kwargs):
    return openai.Completion.create(**kwargs)


def openai_completion(
    prompt: str,
    model: str = "davinci",
    max_tokens: int = 512,
    temperature: float = 0.8,
    stop: str = "\nHuman:",
    n: int = 1,
    best_of: int = 1,
):
    """Generates OpenAI Completion using the provided parameters.

    Args:
        prompt (str): The prompt for generating the completion.
        model (str, optional): The name of the model to use for generating the completion. Defaults to "davinci".
        max_tokens (int, optional): The maximum number of tokens to generate in the completion. Defaults to 512.
        temperature (float, optional): The temperature to use for generating the completion. Defaults to 0.8.
        stop (str, optional): The sequence where the model should stop generating further tokens. Defaults to "\nHuman:".
        n (int, optional): The number of completions to generate. Defaults to 1.
        best_of (int, optional): The number of best completions to return. Defaults to 1.

    Returns:
        response: The generated completion.
    """

    logger.debug(f"Generating OpenAI Completion using prompt: {prompt}")
    logger.debug(
        f"Model: {model}, max_tokens: {max_tokens}, "
        f"temperature: {temperature}, stop: {stop}, n: {n}"
    )

    if not os.environ.get("OPENAI_API_KEY"):
        raise ValueError("OpenAI API key is not available in the environment variable.")

    openai.api_key = os.environ["OPENAI_API_KEY"]
    split_prompt = prompt.split("Human:")
    embeddings = get_openai_embedding(split_prompt[-1])
    logger.debug(embeddings)

    try:
        response = completion_with_backoff(
            engine=model,
            prompt=prompt,
            max_tokens=max_tokens,
            n=n,
            stop=stop,
            best_of=best_of,
            temperature=temperature,
        )
        logger.debug(f"OpenAI Completion: {response}")
        return response
    except Exception as e:
        logger.exception(f"Error in generating OpenAI Completion: {e}")
        raise e from e
