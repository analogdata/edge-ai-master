#!/bin/bash
readonly MODEL_PATH="/home/pi/models/model.tflite"
readonly MAX_TEMP=70

echo "Model path: $MODEL_PATH"
echo "Max temperature: $MAX_TEMP"

# Uncommenting the next line will cause an error because MODEL_PATH is read-only
# MODEL_PATH="/new/path"
