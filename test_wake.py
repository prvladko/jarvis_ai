import pvporcupine
import sounddevice as sd
import numpy as np
import os
from dotenv import load_dotenv
load_dotenv()

ACCESS_KEY = os.getenv("PORCUPINE_ACCESS_KEY")

porcupine = pvporcupine.create(
    access_key=ACCESS_KEY,
    keywords=["jarvis"]
)

print("Listening for wake word...")

def callback(indata, frames, time, status):
    pcm = np.frombuffer(indata, dtype=np.int16)

    result = porcupine.process(pcm)

    if result >= 0:
        print("🔥 WAKE WORD DETECTED")

with sd.InputStream(
    samplerate=porcupine.sample_rate,
    blocksize=porcupine.frame_length,
    dtype="int16",
    channels=1,
    callback=callback
):
    while True:
        pass