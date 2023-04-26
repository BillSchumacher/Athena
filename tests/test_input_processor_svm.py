import pytest

from athena.input_processor import process_input
from athena.nlu.intentions_data import INTENTS, SENTENCES
from athena.nlu.nltk_entities import NLTKEntityExtraction
from athena.nlu.nltk_intent import NLTKIntentClassification

intent_pipeline = NLTKIntentClassification(use_svm=True)
intent_pipeline.train((SENTENCES, INTENTS))
entity_pipeline = NLTKEntityExtraction()


@pytest.mark.skip("SVM is still pretty bad at this.")
def test_process_input_simple():
    user_input = "What's the weather like in Paris?"
    response = process_input(intent_pipeline, entity_pipeline, user_input)
    assert (
        response
        == "I'm not currently able to check the weather, but you asked about Paris."
    )


def test_process_input_empty():
    user_input = ""
    response = process_input(intent_pipeline, entity_pipeline, user_input)
    assert (
        response == "I'm sorry, I didn't receive any input. Can you please try again?"
    )
