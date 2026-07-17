#!/bin/bash
model_file="/home/pi/models/model.tflite"
if [ -f "$model_file" ]; then
    echo "Model file found. Starting inference..."
else
    echo "Model file not found! Please download it first."
    exit 1
fi
