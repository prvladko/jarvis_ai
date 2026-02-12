import wave
import subprocess
from piper import PiperVoice
from config import VOICE_MODEL

voice = PiperVoice.load(VOICE_MODEL)

def speak(text):
    with wave.open("output.wav", "wb") as wav_file:
        voice.synthesize_wav(text, wav_file)

    subprocess.run(["afplay", "output.wav"])