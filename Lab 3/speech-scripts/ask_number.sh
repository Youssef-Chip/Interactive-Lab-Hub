echo "Tell me your favorite number" | python3 -m piper --model en_US-lessac-medium --output-raw | aplay -r 22050 -f S16_LE -t raw -

# Record the response for 5 seconds
arecord -d 5 -f cd -c 1 -r 16000 answer.wav

# Transcribe what was recorded
python3 transcribe.py answer.wav --model base.en