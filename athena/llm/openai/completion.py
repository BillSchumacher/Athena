import os

import openai
from loguru import logger

# Load the API key from the environment variable
openai.api_key = os.environ["OPENAI_API_KEY"]


def openai_completion(
    prompt,
    model="davinci",
    max_tokens=512,
    temperature=0.8,
    stop="\nHuman:",
    n=1,
    best_of=1,
):
    logger.debug(f"Generating OpenAI Completion using prompt: {prompt}")
    logger.debug(
        f"Model: {model}, max_tokens: {max_tokens}, "
        f"temperature: {temperature}, stop: {stop}, n: {n}"
    )
    response = openai.Completion.create(
        engine=model,  # Choose the desired model, e.g., "davinci", "curie", "babbage", "davinci-codex", etc.
        prompt=prompt,
        max_tokens=max_tokens,
        n=n,
        stop=stop,
        best_of=best_of,
        temperature=temperature,
    )
    logger.debug(f"OpenAI Completion: {response}")
    return response.choices[0].text.strip()
