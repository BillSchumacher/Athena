import os
from dotenv import load_dotenv
import openai
from rasa_nlu.training_data import load_data
from rasa_nlu.config import RasaNLUModelConfig
from rasa_nlu.model import Trainer
from rasa_nlu import config
import warnings
from athena.plugins.plugin_manager import PluginManager
from athena.plugins.plugin_base import PluginBase
import plugins  # assuming plugins will be stored in a "plugins" directory/package
from athena.user_manager import UserManager
from athena.plugins.authentication_plugin import AuthenticationPlugin

warnings.filterwarnings('ignore')

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


user_manager = UserManager()
auth_plugin = AuthenticationPlugin(user_manager)


def process_input(user_input, username=None):
    # Use the Rasa NLU interpreter to parse the user input
    parsed_input = interpreter.parse(user_input)

    # Extract intent and entities from the parsed input
    intent = parsed_input["intent"]["name"]
    entities = {entity["entity"]: entity["value"] for entity in parsed_input["entities"]}

    # Create a PluginManager instance, discover the plugins, and process the input using the plugins
    plugin_manager = PluginManager(PluginBase, plugins, extra_plugins=[auth_plugin])
    plugin_manager.discover_plugins()

    if username is not None:
        personalization_data = user_manager.get_user_preference(username, "personalization_data")
        if personalization_data is not None:
            # Apply personalization logic using personalization_data
            pass
    response = plugin_manager.process_input(user_input)
    if response is None:
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

