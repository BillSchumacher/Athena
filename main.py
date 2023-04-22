import os
from dotenv import load_dotenv
import openai

load_dotenv()

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


def process_input(user_input):
    prompt = f"Athena, please help me with the following: {user_input}"
    response = generate_gpt3_response(prompt)
    return response


def main():
    print("Welcome to Athena, the AI Agent. Type 'exit' to end the conversation.")

    while True:
        user_input = input("User: ")

        if user_input.lower() == 'exit':
            print("Athena: Goodbye!")
            break

        response = process_input(user_input)
        print("Athena:", response)


if __name__ == "__main__":
    main()
