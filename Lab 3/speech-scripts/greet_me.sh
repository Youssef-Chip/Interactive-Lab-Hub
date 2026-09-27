#!/bin/bash
echo "Hi Youssef!" | python3 -m piper --model en_US-lessac-medium --output-raw | aplay -r 22050 -f S16_LE -t raw -