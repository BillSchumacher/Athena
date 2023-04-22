import os
from dotenv import load_dotenv
import openai
from rasa_nlu.training_data import load_data
from rasa_nlu.config import RasaNLUModelConfig
from rasa_nlu.model import Trainer
from rasa_nlu import config

training_data = load_data("nlu_data.md")
trainer = Trainer(config.load("nlu_config.yml"))
interpreter = trainer.train(training_data)

# Save the trained model for future use
model_directory = trainer.persist("./models/nlu", fixed_model_name="current")

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
    # Use the Rasa NLU interpreter to parse the user input
    parsed_input = interpreter.parse(user_input)

    # Extract intent and entities from the parsed input
    intent = parsed_input["intent"]["name"]
    entities = {entity["entity"]: entity["value"] for entity in parsed_input["entities"]}

    # Process the user input based on the identified intent and entities
    if intent == "greet":
        response = "Hello! How can I help you today?"
    elif intent == "goodbye":
        response = "Goodbye! Have a great day!"
    elif intent == "ask_weather":
        location = entities.get("location", "unknown")
        response = f"I'm not currently able to check the weather, but you asked about {location}."
    else:
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
