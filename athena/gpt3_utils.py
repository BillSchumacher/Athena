import os
import openai

# Load the API key from the environment variable
openai.api_key = os.environ["OPENAI_API_KEY"]


def generate_gpt3_response(prompt):
    response = openai.Completion.create(
        engine="davinci", # Choose the desired model, e.g., "davinci", "curie", "babbage", "davinci-codex", etc.
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.8,
    )
    return response.choices[0].text.strip()
