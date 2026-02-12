conversation = [
    {
        "role": "system",
        "content": """
You are J.A.R.V.I.S.
Be concise.
If generating Python code, wrap it in ```python``` blocks.
"""
    }
]

def add_user(text):
    conversation.append({"role": "user", "content": text})

def add_assistant(text):
    conversation.append({"role": "assistant", "content": text})

def get_conversation():
    return conversation