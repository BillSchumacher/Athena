from __future__ import annotations

import os
from typing import Optional

try:
    import torch
    from auto_vicuna.__main__ import load_model
    from auto_vicuna.chat import chat_one_shot
    from auto_vicuna.conversation import make_conversation
except ImportError:
    load_model = None
    chat_one_shot = None
    make_conversation = None
    torch = None

from loguru import logger

device = "cuda" if torch and torch.cuda.is_available() else "cpu"
vicuna_weights = os.environ.get("VICUNA_WEIGHTS", "")
load_8bit = os.environ.get("LOAD_8BIT", False)

vicuna_model, tokenizer = (
    load_model(
        vicuna_weights,
        device=device,
        num_gpus=1,
        debug=False,
        load_8bit=load_8bit,
    )
    if load_model
    else (None, None)
)

VICUNA_ERROR = (
    "Vicuna model not loaded, make sure you have the\n"
    "VICUNA_WEIGHTS environment variable set. \n\n"
    "PyTorch, transformers and auto_vicuna must also be installed."
)


def generate_text(
    prompt: str, temperature: float = 0.8, max_tokens: int = 2048
) -> Optional[str]:
    """Generates text using the Vicuna model.

    Args:
        prompt (str): The prompt to generate the text from.
        temperature (float, optional): The temperature to use for text generation.
          Defaults to 0.8.
        max_tokens (int, optional): The maximum number of tokens to generate.
          Defaults to 2048.

    Returns:
        str: The generated text, or None if the Vicuna model was not loaded
          successfully.
    """
    if not vicuna_model or not make_conversation or not chat_one_shot:
        logger.error(VICUNA_ERROR)
        return None

    conv = make_conversation(
        "You are a helpful AI assistant named Athena. You are helping a user named User.",
        ["Athena", "User"],
        [],
    )
    response = chat_one_shot(
        vicuna_model,
        tokenizer,
        vicuna_weights,
        device,
        conv,
        prompt,
        temperature,
        max_tokens,
    )
    logger.debug(f"Vicuna response: {response}")
    return response
