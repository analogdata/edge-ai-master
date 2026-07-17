#!/bin/bash
# Monitor temperature every 5 seconds forever
# Stop with Ctrl + C
# Note: vcgencmd is Raspberry Pi specific — replace with your temp command
while true; do
    # On Raspberry Pi:
    # temp=$(vcgencmd measure_temp | cut -d= -f2)
    # On other systems (macOS/Linux), use a dummy value:
    temp=$(date '+%H:%M:%S')
    echo "Tick: $temp"
    sleep 5
done
