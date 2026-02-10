import wave
from piper import PiperVoice

# Load voice model (path to the .onnx file)
voice = PiperVoice.load("en_US-lessac-medium.onnx")

# Synthesize text to a WAV file
with wave.open("output.wav", "wb") as wav_file:
    voice.synthesize_wav(
        "Hello, I am JARVIS. and I am talking!",
        wav_file
    )

print("Saved output.wav")