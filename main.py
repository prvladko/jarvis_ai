from audio.wake import wait_for_wake_word
from audio.recorder import record_audio
from ai.assistant import ask
from exec.extractor import extract_code
from exec.runner import run
from tts.speaker import speak
import subprocess

def transcribe():
    result = subprocess.run(
        ["whisper-cli", "-m", "/Users/vladkolinko/whisper_models/ggml-base.en.bin", "-f", "input.wav"],
        capture_output=True,
        text=True
    )
    return result.stdout.strip()

def save_code(code):
    filename = "generated_app.py"
    with open(filename, "w") as f:
        f.write(code)
    return filename

def main():
    while True:
        wait_for_wake_word()
        speak("Yes?")

        record_audio()
        text = transcribe()

        if text.lower() in ["exit", "quit"]:
            speak("Going to sleep.")
            continue

        reply = ask(text)
        print(reply)
        speak(reply)

        code = extract_code(reply)
        if code:
            filename = save_code(code)
            output, error = run(filename)

            if output:
                print(output)
            if error:
                print(error)

if __name__ == "__main__":
    main()