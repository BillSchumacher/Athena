from typing import Dict, Tuple, Union
from flask import Blueprint, Response, current_app, jsonify, request
from loguru import logger

from athena.input_processor import process_input

chat_api = Blueprint("chat_api", __name__)


@chat_api.route("/athena", methods=["POST"])
def athena_chat() -> Union[Response, Tuple[Response, int], Tuple[Dict[str, str], int]]:
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
            return jsonify({"response": response})
        else:
            return jsonify({"error": "Missing input"}), 400
    except Exception as e:
        logger.exception(f"Error in processing user input: {e}")
        return jsonify({"error": "Error in processing user input"}), 500
