import requests


def fastchat_chat_completion(
    model,
    messages,
    temperature=0.8,
    max_tokens=512,
):
    resp = requests.post(
        "http://fastchat-api-server:8000/v1/chat/completions",
        json={
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        },
    )
    return resp.text
