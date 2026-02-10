import sounddevice as sd
from scipy.io.wavfile import write

RATE = 44100
SECONDS = 6

print("Speak now...")
audio = sd.rec(int(RATE * SECONDS), samplerate=RATE, channels=1)
sd.wait()

write("input.wav", RATE, audio)
print("Saved input.wav")