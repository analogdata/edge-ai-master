#!/bin/bash
echo "Enter your name:"
read name
echo "Do you want to run inference now? (yes/no):"
read answer
if [ "$answer" = "yes" ]; then
    echo "Starting inference for $name..."
else
    echo "OK, exiting."
fi
