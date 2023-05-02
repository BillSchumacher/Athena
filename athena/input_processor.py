import json

from loguru import logger

import plugins
from athena.llm.fast_chat.chat_completion import fastchat_chat_completion
from athena.llm.openai.completion import openai_completion
from athena.plugins.authentication_plugin import AuthenticationPlugin
from athena.plugins.plugin_base import PluginBase
from athena.plugins.plugin_manager import PluginManager
from athena.prompt import ROLE_ASSISTANT_PROMPT, ROLE_SYSTEM_PROMPT, SYSTEM_PROMPT
from athena.user_manager import UserManager

user_manager = UserManager()
auth_plugin = AuthenticationPlugin(user_manager)


def process_input(
    intent_pipelein,
    entity_pipeline,
    user_input,
    username=None,
    completion_callback=None,
):
    if not completion_callback:
        completion_callback = fastchat_chat_completion
    logger.info(f"User input received: {user_input}")
    if user_input == "":
        return "I'm sorry, I didn't receive any input. Can you please try again?"
    # Use the Rasa NLU interpreter to parse the user input
    parsed_input = intent_pipelein(user_input)
    logger.debug(f"Parsed input: {parsed_input}")

    # Extract intent and entities from the parsed input
    intent, intent_confidence = parsed_input
    entities = entity_pipeline(user_input)
    logger.debug(
        f"Parsed intent: {intent} confidence: {intent_confidence} entities: {entities}"
    )

    # Create a PluginManager instance, discover the plugins, and process the input using the plugins
    plugin_manager = PluginManager(PluginBase, plugins, extra_plugins=[auth_plugin])
    plugin_manager.discover_plugins()

    if username is not None:
        logger.debug(f"User {username} is logged in. Applying personalization...")
        personalization_data = user_manager.get_user_preference(
            username, "personalization_data"
        )
        if personalization_data is not None:
            logger.debug(f"Personalization data found: {personalization_data}")
            # Apply personalization logic using personalization_data
        else:
            logger.debug("No personalization data found.")

    response = plugin_manager.process_input(user_input)
    if completion_callback == openai_completion:
        prompt = f"{SYSTEM_PROMPT}{user_input}"
    else:
        prompt = [
            {"role": "system", "content": ROLE_SYSTEM_PROMPT},
            {"role": "assistant", "content": ROLE_ASSISTANT_PROMPT},
            {"role": "user", "content": user_input},
        ]
    if response is None and intent_confidence < 0.65:
        logger.debug(
            "No plugin was able to process the input and the intent confidence is low. Using GPT-3 to generate a response."
        )
        if completion_callback == fastchat_chat_completion:
            response = completion_callback(
                "fastchat-t5-3b-v1.0", prompt, temperature=0.8, max_tokens=512
            )
        else:
            response = completion_callback(prompt)

    if response is None:
        logger.debug("No plugin was able to process the input. Using default logic.")
        if intent == "greeting":
            response = json.dumps(
                {"choices": [{"text": "Hello! How can I help you today?"}]}
            )
        elif intent == "goodbye":
            response = json.dumps({"choices": [{"text": "Goodbye! Have a great day!"}]})
        elif intent == "current_state":
            response = json.dumps({"choices": [{"text": "I've been busy!"}]})
        elif intent == "name":
            response = json.dumps({"choices": [{"text": "My name is Athena!"}]})
        elif intent == "weather":
            location = "unknown"
            if entities:
                for entity in entities:
                    if entity[0] == "GPE":
                        location = entities[0][-1]
            response = json.dumps(
                {
                    "choices": [
                        {
                            "text": f"I'm not currently able to check the weather, but you asked about {location}."
                        }
                    ]
                }
            )
        elif completion_callback == fastchat_chat_completion:
            logger.debug(
                "No intent was detected. Using fast-chat to generate a response."
            )
            response = completion_callback(
                "fastchat-t5-3b-v1.0", prompt, temperature=0.8, max_tokens=512
            )
        else:
            logger.debug(
                "No intent was detected. Using GPT-3 to generate a response."
            )
            response = completion_callback(prompt)
    logger.info(f"Response generated: {response}")
    return response
