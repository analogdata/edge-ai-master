#!/usr/bin/env python3
"""
06 — Two Service Compose: Producer
Analog Data — EdgeAI Engineering Bootcamp

This is the "producer" service. It generates sensor-like readings
every 3 seconds and writes them to a shared file inside a Docker volume.

The "consumer" service reads from the same file.

This demonstrates how two containers in the same docker-compose.yml
can share data through a named volume.
"""

import json
import os
import random
import sys
import time

# Path to the shared data file (inside the Docker volume)
DATA_FILE = os.environ.get("DATA_FILE", "/shared/data.json")

# Ensure the directory exists
os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

print("Producer starting...")
print(f"Writing sensor data to: {DATA_FILE}")
print()

reading_count = 0
while True:
    reading_count += 1

    # Simulate a sensor reading (temperature in Celsius)
    temperature = round(random.uniform(20.0, 35.0), 2)
    humidity = round(random.uniform(30.0, 70.0), 2)

    # Create the data record
    record = {
        "id": reading_count,
        "temperature": temperature,
        "humidity": humidity,
        "timestamp": time.time(),
    }

    # Write the record to the shared file
    # The consumer service reads from this same file
    with open(DATA_FILE, "w") as f:
        json.dump(record, f)

    print(f"[Producer] Reading #{reading_count:04d} — temp={temperature}°C, humidity={humidity}%")
    sys.stdout.flush()

    time.sleep(3)
