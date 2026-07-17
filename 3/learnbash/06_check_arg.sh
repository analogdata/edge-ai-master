#!/bin/bash
# Usage: ./check_arg.sh <name>
if [ -z "$1" ]; then
    echo "Error: Please provide a name."
    echo "Usage: ./check_arg.sh <name>"
    exit 1
fi
echo "Hello, $1!"
