from typing import Any, Dict, Tuple, Union

from flask import current_app, request
from flask_restx import Namespace, Resource, fields
from loguru import logger

from athena.input_processor import process_input

chat_api = Namespace("chat", description="chat related operations")

chat = chat_api.model(
    "Chat",
    {
        "response": fields.String(required=True, description="The response"),
        "error": fields.String(required=True, description="The error"),
    },
)


@chat_api.route("/athena")
class Chat(Resource):
    @chat_api.doc("athena_chat")
    @chat_api.marshal_list_with(chat)
    def post(self) -> Union[Dict[str, Any], Tuple[Dict[str, Any], int]]:
        """API endpoint to receive user input and return the response from Athena.

        Returns:
            A JSON response with the response message or an error message.
        """
        logger.debug("Received request to chat with Athena")
        data = request.get_json(force=True)
        user_input = data.get("input")
        username = data.get("username", None)
        logger.debug(f"User input: {user_input} Username: {username}")
        input_pipeline_extension = current_app.extensions["input_pipeline"]
        try:
            if user_input:
                response = process_input(
                    input_pipeline_extension.intent_pipeline,
                    input_pipeline_extension.entity_pipeline,
                    user_input,
                    username,
                )
                return {"response": response, "error": None}
            else:
                return {"response": None, "error": "Missing input"}, 400
        except Exception as e:
            logger.exception(f"Error in processing user input: {e}")
        return {"response": None, "error": "Error in processing user input"}, 500
