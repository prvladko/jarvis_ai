import subprocess
import re
import sounddevice as sd
from scipy.io.wavfile import write
from config import RATE, WAKE_SECONDS, MODEL_PATH
from rapidfuzz import fuzz

def wait_for_wake_word():
    print("👂 Listening for wake word...")

    while True:
        audio = sd.rec(int(RATE * WAKE_SECONDS), samplerate=RATE, channels=1)
        sd.wait()
        write("wake.wav", RATE, audio)

        result = subprocess.run(
            ["whisper-cli", "-m", MODEL_PATH, "-f", "wake.wav"],
            capture_output=True,
            text=True
        )

        heard_raw = result.stdout.lower()
        heard = re.sub(r"\[.*?\]", "", heard_raw)
        heard = re.sub(r"[^\w\s]", "", heard).strip()

        WAKE_WORD = "jarvis"

        similarity = fuzz.ratio(heard, WAKE_WORD)

        print(f"Heard: {heard} | similarity: {similarity}")

        if similarity > 70:
            print("✅ Wake word detected")
            return