#!/usr/bin/env bash
set -e

TS=$(date +"%Y%m%d_%H%M%S")
PIANO_OUT="piano_${TS}.wav"
REF_OUT="ref_${TS}.wav"

IN_DEV="alsa_input.usb-Burr-Brown_from_TI_USB_Audio_CODEC-00.analog-stereo-input"
MON_DEV="alsa_output.usb-Burr-Brown_from_TI_USB_Audio_CODEC-00.analog-stereo-output.monitor"

echo "Starting synchronized recording..."
echo "  Piano -> ${PIANO_OUT}"
echo "  Ref   -> ${REF_OUT}"
echo "Press ENTER or Ctrl+C to stop both."

ffmpeg -loglevel error -f pulse -i "$IN_DEV" -c:a pcm_s16le -ar 48000 -ac 2 "$PIANO_OUT" &
PID1=$!

ffmpeg -loglevel error -f pulse -i "$MON_DEV" -c:a pcm_s16le -ar 48000 -ac 2 "$REF_OUT" &
PID2=$!

cleanup() {
  echo ""
  echo "Stopping recordings..."
  kill -INT "$PID1" "$PID2" 2>/dev/null || true
  wait "$PID1" "$PID2" 2>/dev/null || true
  echo "Saved: ${PIANO_OUT} and ${REF_OUT}"
}

trap cleanup EXIT INT TERM

# Wait until user presses Enter or sends Ctrl+C
read -r _ || true