import os
import click
from flask import Flask
from flask_cors import CORS
from athena.loguru_config import setup_logging
from athena.api_views.chat import chat_api


app = Flask(__name__)
CORS(app)  # , origins=["http://localhost:3000"])
app.register_blueprint(chat_api, url_prefix="/api/v1")


@click.command()
@click.option(
    "--log-level",
    type=str,
    default=os.getenv("LOG_LEVEL", "INFO"),
    help="Set logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
)
def main(log_level) -> None:
    setup_logging(log_level)
    app.run(host='0.0.0.0', port=5000)


if __name__ == '__main__':
    main()
