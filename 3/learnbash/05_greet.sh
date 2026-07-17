#!/bin/bash
# save as greet.sh
# Usage: ./greet.sh <name> <city>
name=$1
city=$2
echo "Hello, $name!"
echo "You are from $city."
echo "Script name: $0"
echo "Total arguments received: $#"
