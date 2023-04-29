from typing import List

OPENAI_COMPLETION_MODELS: List[str] = [
    "text-davinci-003",
    "text-davinci-002",
    "text-curie-001",
    "text-babbage-001",
    "text-ada-001",
]

OPENAI_CHAT_COMPLETION_MODELS: List[str] = [
    "gpt-4",
    "gpt-4-0314",
    "gpt-4-32k",
    "gpt-4-32k-0314",
    "gpt-3.5-turbo",
    "gpt-3.5-turbo-0301",
]

OPENAI_EDITS_MODELS: List[str] = ["text-davinci-edit-001", "code-davinci-edit-001"]

OPENAI_AUDIO_TRANSCRIPTION_MODELS: List[str] = ["whisper-1"]

OPENAI_AUDIO_TRANSLATION_MODELS: List[str] = ["whisper-1"]

OPENAI_FINE_TUNE_MODELS: List[str] = [
    "davinci",
    "curie",
    "babbage",
    "ada",
]

OPENAI_EMBEDDING_MODELS: List[str] = [
    "text-embedding-ada-002",
    "text-search-ada-doc-001",
]

OPENAI_TEXT_MODERATION_MODELS: List[str] = [
    "text-moderation-stable",
    "text-moderation-latest",
]
