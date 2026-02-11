import sounddevice as sd
from scipy.io.wavfile import write
import subprocess
import requests
import json
import time

# -------- CONFIG --------
RATE = 44100
SECONDS = 6
MODEL_PATH = "/Users/vladkolinko/whisper_models/ggml-base.en.bin"
OLLAMA_MODEL = "qwen2.5-coder:7b"
# ------------------------

def record_audio():
    print("🎙 Speak now...")
    audio = sd.rec(int(RATE * SECONDS), samplerate=RATE, channels=1)
    sd.wait()
    write("input.wav", RATE, audio)
    print("✅ Audio recorded")

def transcribe_audio():
    print("📝 Transcribing...")
    command = [
        "whisper-cli",
        "-m", MODEL_PATH,
        "-f", "input.wav"
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout.strip()

def ask_jarvis(text):
    print("🧠 Thinking...")
    prompt = f"""
If user asks to create code:
- Put ONLY the final Python code inside triple backticks.
- Example:

```python
print("hello")

User said:
{text}
"""
    

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]

def extract_code(response_text):
    pattern = r"```python(.*?)```"
    match = re.search(pattern, response_text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None

def save_code(code):
    filename = "generated_app.py"
    with open(filename, "w") as f:
        f.write(code)
    print(f"\n📁 Code saved to {filename}")

def main():
    record_audio()
    text = transcribe_audio()

    print("\n🗣 You said:")
    print(text)

    answer = ask_jarvis(text)

    print("\n🤖 J.A.R.V.I.S:\n")
    print(answer)

if __name__ == "__main__":
    main()