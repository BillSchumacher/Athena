from athena.input_processor import process_input


def test_process_input_simple():
    user_input = "What is the capital of France?"
    response = process_input(user_input)
    assert response == "The capital of France is Paris."


def test_process_input_empty():
    user_input = ""
    response = process_input(user_input)
    assert response == "I'm sorry, I didn't receive any input. Can you please try again?"
