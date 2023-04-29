import os

import click
from flask import Flask
from flask_cors import CORS

from athena.api_views import blueprint as api
from athena.loguru_config import setup_logging
from athena.nlu.intentions_data import INTENTIONS_TRAIN_DATA, INTENTS, SENTENCES
from athena.nlu.nltk_entities import NLTKEntityExtraction
from athena.nlu.nltk_intent import NLTKIntentClassification

app = Flask(__name__)

CORS(app)  # , origins=["http://localhost:3000"])


class InputPipelineExtension:
    def __init__(self, app=None):
        self.intent_pipeline = None
        self.entity_pipeline = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        if os.getenv("USE_SVM", "True") == "True":
            self.intent_pipeline = NLTKIntentClassification(use_svm=True)
            self.intent_pipeline.train((SENTENCES, INTENTS))
        else:
            self.intent_pipeline = NLTKIntentClassification()
            self.intent_pipeline.train(INTENTIONS_TRAIN_DATA)
        self.entity_pipeline = NLTKEntityExtraction()


@click.command()
@click.option(
    "--log-level",
    type=str,
    default=os.getenv("LOG_LEVEL", "INFO"),
    help="Set logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
)
def main(log_level) -> None:
    setup_logging(log_level)
    from athena.db import engine
    from athena.models import api as models

    models.Base.metadata.create_all(bind=engine)

    input_extension = InputPipelineExtension(app)
    app.extensions["input_pipeline"] = input_extension
    app.register_blueprint(api, url_prefix="/api/v1")
    app.run(host="0.0.0.0", port=5000)


if __name__ == "__main__":
    main()
