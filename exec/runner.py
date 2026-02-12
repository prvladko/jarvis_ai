import subprocess

def run(filename):
    result = subprocess.run(
        ["python3", filename],
        capture_output=True,
        text=True,
        timeout=10
    )

    return result.stdout, result.stderr