#!/bin/bash
set -u

model_path="/home/pi/models/model.tflite"
# The next line uses a typo (model_pth instead of model_path)
# With set -u, the script stops immediately with: "model_pth: unbound variable"
# Without set -u, Bash would silently print nothing — no error
echo "Model path is: $model_path"
echo "This line runs fine."

# Uncomment the next line to see set -u catch the typo:
# echo $model_pth
