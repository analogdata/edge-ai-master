#!/bin/bash
# Loop over all .tflite model files in the models directory
# Change the path to match your system
for file in /home/pi/models/*.tflite; do
    echo "Found model: $file"
done

# Generic version — loop over all files in current directory
# for file in *; do
#     echo "Found: $file"
# done
