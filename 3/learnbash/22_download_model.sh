#!/bin/bash
set -euo pipefail
# =====================================================
# Model Download and Verification Script
# Usage: ./download_model.sh <url> <expected_sha256>
# Example:
#   ./download_model.sh \
#     https://example.com/model.tflite \
#     a3f9c2d1e8b74f6...
# =====================================================
# Check arguments
if [ "$#" -ne 2 ]; then
    echo "ERROR: Wrong number of arguments."
    echo "Usage: $0 <download_url> <expected_sha256_hash>"
    exit 1
fi
DOWNLOAD_URL="$1"
EXPECTED_HASH="$2"
DOWNLOAD_DIR="/home/pi/models"
FILENAME=$(basename "$DOWNLOAD_URL")    # extract filename from URL
FILEPATH="$DOWNLOAD_DIR/$FILENAME"
echo "======================================="
echo " Model Download & Verification Script"
echo "======================================="
echo "URL      : $DOWNLOAD_URL"
echo "Filename : $FILENAME"
echo "Save to  : $FILEPATH"
echo ""
# --- Step 1: Create models directory if it doesn't exist ---
if [ ! -d "$DOWNLOAD_DIR" ]; then
    echo "Creating directory: $DOWNLOAD_DIR"
    mkdir -p "$DOWNLOAD_DIR"
fi
# --- Step 2: Download the file ---
echo "Downloading model..."
wget --show-progress -O "$FILEPATH" "$DOWNLOAD_URL"
echo "Download complete."
echo ""
# --- Step 3: Verify the SHA256 hash ---
echo "Verifying file integrity..."
ACTUAL_HASH=$(sha256sum "$FILEPATH" | awk '{print $1}')
echo "Expected hash : $EXPECTED_HASH"
echo "Actual hash   : $ACTUAL_HASH"
echo ""
if [ "$ACTUAL_HASH" = "$EXPECTED_HASH" ]; then
    echo "✅ Verification PASSED - File is intact."
    echo "Model saved to: $FILEPATH"
else
    echo "❌ Verification FAILED - File is corrupted or tampered!"
    echo "Deleting the bad file..."
    rm -f "$FILEPATH"
    exit 1
fi
echo ""
echo "Done! Model is ready to use."
