from athena.plugins.plugin_manager import PluginManager
from athena.plugins.plugin_base import PluginBase
import plugins  # assuming plugins will be stored in a "plugins" directory/package
from athena.gpt3_utils import generate_gpt3_response
from athena.nlu_utils import interpreter
from athena.user_manager import UserManager
from athena.plugins.authentication_plugin import AuthenticationPlugin

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
