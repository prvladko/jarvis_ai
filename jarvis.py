import sounddevice as sd
from scipy.io.wavfile import write
import subprocess
import requests
import json
import time
import re
import wave
from piper import PiperVoice
import subprocess
from rapidfuzz import fuzz

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


# -------- CONFIG --------
RATE = 44100
SECONDS = 6
MODEL_PATH = "/Users/vladkolinko/whisper_models/ggml-base.en.bin"
OLLAMA_MODEL = "qwen2.5-coder:7b"
WAKE_WORD = "jarvis"
WAKE_SECONDS = 3
# ------------------------
voice = PiperVoice.load("en_US-lessac-medium.onnx")

def wait_for_wake_word():
    print("👂 Listening for wake word...")

    while True:
        audio = sd.rec(int(RATE * WAKE_SECONDS), samplerate=RATE, channels=1)
        sd.wait()
        write("wake.wav", RATE, audio)

        command = [
            "whisper-cli",
            "-m", MODEL_PATH,
            "-f", "wake.wav"
        ]

        result = subprocess.run(command, capture_output=True, text=True)
        heard_raw = result.stdout.lower()

        # remove timestamps
        heard = re.sub(r"\[.*?\]", "", heard_raw)

        # remove punctuation
        heard = re.sub(r"[^\w\s]", "", heard)

        heard = heard.strip()

        words = heard.split()

        detected = False

        for word in words:
            similarity = fuzz.partial_ratio(word, WAKE_WORD)
            print(f"Heard word: {word} | similarity: {similarity}")

            if similarity >= 75:
                detected = True
                break

        if detected:
            print("✅ Wake word detected")
            speak("Yes?")
            break

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

def ask_jarvis(user_text):
    global conversation

    conversation.append({
        "role": "user",
        "content": user_text
    })

    print("🧠 Thinking...")

    response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": OLLAMA_MODEL,
            "messages": conversation,
            "stream": False
        }
    )

    assistant_reply = response.json()["message"]["content"]

    conversation.append({
        "role": "assistant",
        "content": assistant_reply
    })

    return assistant_reply

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

    run_generated_code(filename)

def run_generated_code(filename):
    print("▶️ Running generated code...\n")

    try:
        result = subprocess.run(
            ["python3", filename],
            capture_output=True,
            text=True,
            timeout=10
        )

        output = result.stdout
        errors = result.stderr

        if output:
            print("📤 Output:\n", output)

        if errors:
            print("⚠️ Errors:\n", errors)

        if output:
            speak("The program executed successfully.")
        elif errors:
            speak("There was an error in the generated code.")

    except subprocess.TimeoutExpired:
        print("⏰ Execution timed out.")
        speak("The program took too long to run.")

def speak(text):
    print("🔊 Speaking...")
    with wave.open("output.wav", "wb") as wav_file:
        voice.synthesize_wav(text, wav_file)

    subprocess.run(["afplay", "output.wav"])

def main():
    while True:
        wait_for_wake_word()

        record_audio()
        text = transcribe_audio()

        print("\n🗣 You said:")
        print(text)

        if text.lower() in ["exit", "quit", "stop"]:
            speak("Going back to sleep.")
            continue

        answer = ask_jarvis(text)

        print("\n🤖 J.A.R.V.I.S:\n")
        print(answer)

        speak(answer)

        code = extract_code(answer)
        if code:
            save_code(code)

if __name__ == "__main__":
    main()