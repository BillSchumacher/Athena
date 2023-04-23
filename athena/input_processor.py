from athena.plugins.plugin_manager import PluginManager
from athena.plugins.plugin_base import PluginBase
import plugins
from athena.gpt3_utils import generate_gpt3_response
from athena.nlu_utils import predict_intent
from athena.user_manager import UserManager
from athena.plugins.authentication_plugin import AuthenticationPlugin
from loguru import logger

user_manager = UserManager()
auth_plugin = AuthenticationPlugin(user_manager)


def process_input(nlp, user_input, username=None):
    logger.info(f"User input received: {user_input}")
    # Use the Rasa NLU interpreter to parse the user input

    parsed_input = predict_intent(nlp, user_input)
    logger.debug(f"Parsed input: {parsed_input}")

    # Extract intent and entities from the parsed input
    intent = parsed_input["intent"]["name"]
    intent_confidence = parsed_input["intent"]["confidence"]
    entities = {entity["entity"]: entity["value"] for entity in parsed_input["entities"]}
    logger.debug(f"Parsed intent: {intent} confidence: {intent_confidence} entities: {entities}")

    # Create a PluginManager instance, discover the plugins, and process the input using the plugins
    plugin_manager = PluginManager(PluginBase, plugins, extra_plugins=[auth_plugin])
    plugin_manager.discover_plugins()

    if username is not None:
        logger.debug(f"User {username} is logged in. Applying personalization...")
        personalization_data = user_manager.get_user_preference(username, "personalization_data")
        if personalization_data is not None:
            logger.debug(f"Personalization data found: {personalization_data}")
            # Apply personalization logic using personalization_data
        else:
            logger.debug("No personalization data found.")

    response = plugin_manager.process_input(user_input)

    if response is None and intent_confidence < 0.65:
        logger.debug("No plugin was able to process the input and the intent confidence is low. Using GPT-3 to generate a response.")
        prompt = f"Athena, please help me with the following: {user_input}"
        response = generate_gpt3_response(prompt)

    if response is None:
        logger.debug("No plugin was able to process the input. Using default logic.")
        if intent == "greet":
            response = "Hello! How can I help you today?"
        elif intent == "goodbye":
            response = "Goodbye! Have a great day!"
        elif intent == "ask_weather":
            location = entities.get("location", "unknown")
            response = f"I'm not currently able to check the weather, but you asked about {location}."
        else:
            logger.debug("No intent was detected. Using GPT-3 to generate a response.")
            prompt = f"Athena, please help me with the following: {user_input}"
            response = generate_gpt3_response(prompt)
    logger.info(f"Response generated: {response}")
    return response
