from flask import Blueprint
from flask_restx import Api

from .chat import chat_api

blueprint = Blueprint("api", __name__)
api = Api(
    blueprint,
    version="0.0.12",
    title="Athena API",
    description="An autonomous AI agent API",
)

api.add_namespace(chat_api)
