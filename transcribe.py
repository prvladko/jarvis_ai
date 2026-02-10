import subprocess

command = [
    "whisper",
    "-m", "base.en",
    "-f", "input.wav"
]

result = subprocess.run(command, capture_output=True, text=True)

print("You said:")
print(result.stdout)