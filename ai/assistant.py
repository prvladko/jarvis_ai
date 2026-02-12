import requests
from config import OLLAMA_MODEL
from ai.memory import add_user, add_assistant, get_conversation

def ask(user_text):
    add_user(user_text)

    response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": OLLAMA_MODEL,
            "messages": get_conversation(),
            "stream": False
        }
    )

    reply = response.json()["message"]["content"]
    add_assistant(reply)

    return reply