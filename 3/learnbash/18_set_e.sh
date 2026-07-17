#!/bin/bash
set -e

echo "Downloading model..."
# wget https://example.com/model.tflite    # if this fails...
echo "Starting inference..."             # ...this line NEVER runs (with -e)
echo "python3 run_inference.py"          # ...and this never runs either
echo "Demo: with set -e, the script stops on the first failed command."
echo "Uncomment the wget line above with a bad URL to see it in action."
