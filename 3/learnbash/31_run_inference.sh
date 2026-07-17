#!/bin/bash
set -euo pipefail
# =====================================================
# Run Inference — A simple inference runner script
# Usage: ./run_inference.sh [model_path] [image_path]
# =====================================================

MODEL_PATH="${1:-/home/pi/models/model.tflite}"
IMAGE_PATH="${2:-/home/pi/captures/latest.jpg}"

# Colour codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}ℹ️  Starting inference...${NC}"

# Check if model file exists
if [ ! -f "$MODEL_PATH" ]; then
    echo -e "${RED}❌ Error: Model file not found at $MODEL_PATH${NC}"
    exit 1
fi

# Check if image file exists
if [ ! -f "$IMAGE_PATH" ]; then
    echo -e "${RED}❌ Error: Image file not found at $IMAGE_PATH${NC}"
    exit 1
fi

echo -e "${BLUE}ℹ️  Model : $MODEL_PATH${NC}"
echo -e "${BLUE}ℹ️  Image : $IMAGE_PATH${NC}"

# Run the inference (replace with your actual inference command)
# python3 run_inference.py --model "$MODEL_PATH" --image "$IMAGE_PATH"
echo -e "${YELLOW}⚠️  (Demo mode — uncomment the python3 line to run real inference)${NC}"

echo -e "${GREEN}✅ Inference complete.${NC}"
