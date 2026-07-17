#!/bin/bash
for i in 1 2 3 4 5; do
    echo "Count: $i"
done

# Cleaner way using {start..end}
for i in {1..10}; do
    echo "Number: $i"
done
