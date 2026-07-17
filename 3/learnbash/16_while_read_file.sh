#!/bin/bash
# Read a file line by line
# Creates a demo config file if it doesn't exist

CONFIG_FILE="/tmp/config.txt"

if [ ! -f "$CONFIG_FILE" ]; then
    echo "model=resnet50" > "$CONFIG_FILE"
    echo "threshold=0.85" >> "$CONFIG_FILE"
    echo "device=/dev/video0" >> "$CONFIG_FILE"
    echo "Created demo $CONFIG_FILE"
fi

while IFS= read -r line; do
    echo "Processing: $line"
done < "$CONFIG_FILE"
