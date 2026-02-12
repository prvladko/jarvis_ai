import sounddevice as sd
from scipy.io.wavfile import write
from config import RATE, SECONDS

def record_audio(filename="input.wav"):
    audio = sd.rec(int(RATE * SECONDS), samplerate=RATE, channels=1)
    sd.wait()
    write(filename, RATE, audio)