WEATHER_TRAIN_DATA = [
    ("weather like today?", "weather"),
    ("weather like tomorrow?", "weather"),
    ("weather like in London?", "weather"),
    ("weather be like tomorrow?", "weather"),
    ("weather be like in London?", "weather"),
    ("weather be like over the weekend?", "weather"),
    ("weather be like in New York?", "weather"),
    ("weather be like in London over the weekend?", "weather"),
    ("weather be like in Berlin next week?", "weather"),
    ("weather be like in New York for the next 24 hours?", "weather"),
    ("weather be like in Paris for the next 48 hours?", "weather"),
    ("weather be like in Madrid for the next 72 hours?", "weather"),
    ("weather in New York?", "weather"),
    ("weather in Chicago over the weekend?", "weather"),
    ("weather in Detroit next week?", "weather"),
    ("weather in Tokyo for the next 24 hours?", "weather"),
    ("weather in New York for the next 48 hours?", "weather"),
    ("weather in Berlin for the next 48 hours?", "weather"),
    ("weather in Paris for the next 72 hours?", "weather"),
    ("weather like in Madrid for the next 3 days?", "weather"),
    ("weather like in London for the next week?", "weather"),
]

GREETING_TRAIN_DATA = [
    ("Hi", "greeting"),
    ("Hello", "greeting"),
    ("Hey", "greeting"),
    ("Hi there", "greeting"),
    ("Hello there", "greeting"),
    ("Hey there", "greeting"),
    ("Good morning", "greeting"),
    ("Good afternoon", "greeting"),
    ("Good evening", "greeting"),
    ("Good day", "greeting"),
    ("Good to see", "greeting"),
    ("Nice to see", "greeting"),
]

GOODBYE_TRAIN_DATA = [
    ("Goodbye", "goodbye"),
    ("Bye", "goodbye"),
    ("Later", "goodbye"),
    ("See you later", "goodbye"),
    ("See you soon", "goodbye"),
    ("See you later alligator", "goodbye"),
    ("See you later crocodile", "goodbye"),
    ("See you later alligator in a while crocodile", "goodbye"),
    ("Have a nice day", "goodbye"),
    ("Have a nice day!", "goodbye"),
    ("Have a nice day.", "goodbye"),
]

CURRENT_STATE_DATA = [
    ("How are you?", "current_state"),
    ("How is life?", "current_state"),
    ("What's up with you?", "current_state"),
    ("How have you been?", "current_state"),
    ("What are you up to?", "current_state"),
    ("Sup?", "current_state"),
]

NAME_DATA = [
    ("Who are you?", "name"),
    ("What is your name?", "name"),
    ("What can I call you?", "name"),
    ("Do you have a name?", "name"),
]

INTENTION_DATA_SETS = [
    WEATHER_TRAIN_DATA,
    GREETING_TRAIN_DATA,
    GOODBYE_TRAIN_DATA,
    CURRENT_STATE_DATA,
    NAME_DATA,
]
INTENTIONS_TRAIN_DATA = [item for sublist in INTENTION_DATA_SETS for item in sublist]
SENTENCES = []
INTENTS = []
for sentence, intent in INTENTIONS_TRAIN_DATA:
    SENTENCES.append(sentence)
    INTENTS.append(intent)
