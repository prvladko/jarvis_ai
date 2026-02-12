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
import pvporcupine
import os

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
ACCESS_KEY = os.getenv("PORCUPINE_ACCESS_KEY")
RATE = 44100
SECONDS = 6
MODEL_PATH = "/Users/vladkolinko/whisper_models/ggml-base.en.bin"
OLLAMA_MODEL = "qwen2.5-coder:7b"
MEMORY_FILE = "conversation_memory.json"
# ------------------------

porcupine = pvporcupine.create(
    access_key=ACCESS_KEY,
    keywords=["jarvis"]
)

voice = PiperVoice.load("en_US-lessac-medium.onnx")

def load_memory():
    global conversation
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            conversation[:] = json.load(f)

def save_memory():
    with open(MEMORY_FILE, "w") as f:
        json.dump(conversation, f, indent=2)

def wait_for_wake_word():
    print("👂 Listening for wake word...")

    detected = False

    def callback(indata, frames, time_info, status):
        nonlocal detected

        pcm = indata.flatten()
        result = porcupine.process(pcm)

        if result >= 0:
            detected = True

    with sd.InputStream(
        samplerate=porcupine.sample_rate,
        blocksize=porcupine.frame_length,
        dtype="int16",
        channels=1,
        callback=callback
    ):
        while not detected:
            sd.sleep(10)

    print("🔥 Wake word detected")
    speak("Yes?")

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
    save_memory()

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
    load_memory()
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