import os
import openai
from loguru import logger


# Load the API key from the environment variable
openai.api_key = os.environ["OPENAI_API_KEY"]


def generate_gpt3_response(prompt, model="davinci", max_tokens=100, temperature=0.8, stop=None, n=1):
    logger.debug(f"Generating GPT-3 response using prompt: {prompt}")
    logger.debug(f"Model: {model}, max_tokens: {max_tokens}, temperature: {temperature}, stop: {stop}, n: {n}")
    response = openai.Completion.create(
        engine=model, # Choose the desired model, e.g., "davinci", "curie", "babbage", "davinci-codex", etc.
        prompt=prompt,
        max_tokens=max_tokens,
        n=n,
        stop=stop,
        temperature=temperature,
    )
    logger.debug(f"GPT-3 response: {response}")
    return response.choices[0].text.strip()
