#!/bin/bash
set -euo pipefail
# =====================================================
# Batch Inference Script — Run inference on all images in a folder
# Usage: ./batch_inference.sh [input_dir] [model_path]
# =====================================================

INPUT_DIR="${1:-/home/pi/captures}"
MODEL_PATH="${2:-/home/pi/models/model.tflite}"

if [ ! -d "$INPUT_DIR" ]; then
    echo "Error: Input directory $INPUT_DIR does not exist."
    exit 1
fi

if [ ! -f "$MODEL_PATH" ]; then
    echo "Error: Model file $MODEL_PATH not found."
    exit 1
fi

echo "======================================"
echo "  Batch Inference Runner"
echo "  $(date)"
echo "======================================"
echo "Input dir : $INPUT_DIR"
echo "Model     : $MODEL_PATH"
echo ""

count=0
for image in "$INPUT_DIR"/*.jpg; do
    if [ ! -f "$image" ]; then
        echo "No .jpg images found in $INPUT_DIR"
        exit 0
    fi
    count=$((count + 1))
    echo "[$count] Running inference on: $(basename "$image")"
    # python3 run_inference.py --model "$MODEL_PATH" --image "$image"
    echo "    -> (demo) inference complete for $(basename "$image")"
done

echo ""
echo "======================================"
echo "Processed $count image(s)."
echo "Done: $(date)"
echo "======================================"
