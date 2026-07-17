#!/bin/bash
count=1
while [ $count -le 5 ]; do
    echo "Loop number: $count"
    count=$((count + 1))    # increment count by 1
done
