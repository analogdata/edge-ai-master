#!/bin/bash
temperature=65
if [ $temperature -gt 70 ]; then
    echo "CRITICAL: Pi is overheating!"
elif [ $temperature -gt 60 ]; then
    echo "WARNING: Temperature is high."
else
    echo "OK: Temperature is normal."
fi
