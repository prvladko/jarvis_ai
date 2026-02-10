import requests
import subprocess

# Transcribe
command = ["whisper", "-m", "base.en", "-f", "input.wav"]
text = subprocess.run(command, capture_output=True, text=True).stdout

prompt = f"""
You are a helpful assistant.
Explain everything step by step for a beginner.
User request: {text}
"""

# Send to Ollama
response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "qwen2.5-coder:7b",
        "prompt": prompt,
        "stream": False
    }
)

print("\nJ.A.R.V.I.S.:\n")
print(response.json()["response"])