import os

import click

from athena.input_processor import process_input
from athena.loguru_config import setup_logging
from athena.nlu.intentions_data import INTENTIONS_TRAIN_DATA
from athena.nlu.nltk_entities import NLTKEntityExtraction
from athena.nlu.nltk_intent import NLTKIntentClassification


@click.command()
@click.option(
    "--log-level",
    type=str,
    default=os.getenv("LOG_LEVEL", "INFO"),
    help="Set logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
)
def main(log_level):
    setup_logging(log_level)
    from loguru import logger

    logger.info("Welcome to Athena!")
    username = input("Please enter your name: ")
    intent_pipeline = NLTKIntentClassification()
    intent_pipeline.train(INTENTIONS_TRAIN_DATA)
    entity_pipeline = NLTKEntityExtraction()
    from athena.db import engine
    from athena.models import api as models

    models.Base.metadata.create_all(bind=engine)

    try:
        while True:
            user_input = input(f"{username}: ")
            if user_input.lower() in ["exit", "quit"]:
                break

            response = process_input(
                intent_pipeline, entity_pipeline, user_input, username
            )
            logger.info(f"{response}")
    except KeyboardInterrupt:
        pass
    logger.info("Athena: Goodbye!")


if __name__ == "__main__":
    main()
