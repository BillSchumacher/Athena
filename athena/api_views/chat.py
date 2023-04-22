from flask import Blueprint, request, jsonify
from athena.input_processor import process_input
from loguru import logger

chat_api = Blueprint("chat_api", __name__)


@chat_api.route("/athena", methods=["POST"])
def athena_chat():
    logger.debug("Received request to chat with Athena")
    data = request.get_json(force=True)
    user_input = data.get('input')
    username = data.get('username', None)
    logger.debug(f"User input: {user_input} Username: {username}")

    if user_input:
        response = process_input(user_input, username)
        return jsonify({'response': response})
    else:
        return jsonify({'error': 'Missing input'}), 400
