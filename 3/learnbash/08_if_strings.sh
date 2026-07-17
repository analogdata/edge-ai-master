#!/bin/bash
status="running"
if [ "$status" = "running" ]; then
    echo "Service is active"
elif [ "$status" = "stopped" ]; then
    echo "Service is down"
fi
