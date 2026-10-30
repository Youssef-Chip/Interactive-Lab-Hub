import time
import json
import datetime
from collections import Counter
import sounddevice as sd
import numpy as np
import qwiic_button
import requests
import os

THRESHOLD = 12.0
LOG_FILE = "audio_log.jsonl"
MODEL = "qwen3.5:0.8b"

button = qwiic_button.QwiicButton()
if not button.begin():
    print("Error: Qwiic Button not connected.")
    exit(1)


open(LOG_FILE, "w").close()


def write_log(entry):
    with open(LOG_FILE, "a") as log:
        log.write(json.dumps(entry) + "\n")


# Phase 1: Wait for Bedtime
print("System ready. Press the glowing button to start tracking...")
button.LED_on(255)

while not button.is_button_pressed():
    time.sleep(0.1)

print("Night shift started. LED dimming. Goodnight and Sweet Dreams!")
button.LED_off()
time.sleep(1.5)

# Phase 2: The Night Shift (Audio Tracking)


def audio_callback(indata, frames, time_info, status):
    volume = np.linalg.norm(indata) * 10
    if volume > THRESHOLD:
        now = datetime.datetime.now().isoformat(timespec="seconds")
        print(f"Spike detected! {volume:.1f} dB at {now}")
        write_log({"t": now, "volume": round(volume, 1)})


stream = sd.InputStream(callback=audio_callback)
with stream:
    # Wait for the user to wake up and press the button again
    while not button.is_button_pressed():
        time.sleep(0.1)

# Phase 3: The Morning Reveal
print("\nGood morning! Button pressed. Stopping tracking...")
button.LED_on(255)

# Read the log we just made
try:
    entries = [json.loads(line) for line in open(LOG_FILE) if line.strip()]
except FileNotFoundError:
    entries = []

if not entries:
    report = "Quiet night. I heard absolutely nothing, you slept perfectly."
else:
    print("Asking Qwen to analyze your sleep...")

    spike_count = len(entries)
    if spike_count <= 2:
        verdict = "mostly restful"
    elif spike_count <= 5:
        verdict = "somewhat restless"
    else:
        verdict = "very restless"

    # PRE-PROCESS TIMES IN PYTHON
    hours = []
    for e in entries:
        dt = datetime.datetime.fromisoformat(e['t'])
        hours.append(dt.strftime("%I %p").lstrip("0"))

    most_common_hour = Counter(hours).most_common(1)[0][0]

    prompt = f"""You are a bedside sleep tracker speaking to your user. Write a natural, two-sentence morning greeting summarizing their sleep.

Here are the facts you must use:
- The user had {spike_count} noise spikes last night.
- Therefore, the night was {verdict}.
- The most noise happened around {most_common_hour}.

Rules:
- Say 'you', not 'I'.
- Do not mention decibels or make up exact times."""

    try:
        r = requests.post("http://localhost:11434/api/generate", json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.4,
                "num_predict": 150
            },
        }, timeout=180)

        response_data = r.json()

        report = response_data["response"].replace('\n', ' ').strip()

        # Fallback if the model genuinely outputs nothing
        if not report:
            report = f"Good morning, you had {spike_count} spikes last night, making it {verdict}. Most spikes were around 3 AM"

    except Exception as e:
        print("Error connecting:", e)

print("\nReport:", report)

# Speak the report out loud using Piper
os.system(f'echo "{report}" | piper --model en_US-lessac-medium.onnx --output-raw | aplay -D plughw:2,0 -r 22050 -f S16_LE -t raw -')

print("Done. Have a great day!")
