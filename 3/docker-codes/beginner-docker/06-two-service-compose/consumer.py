#!/usr/bin/env python3
"""
06 — Two Service Compose: Consumer
Analog Data — EdgeAI Engineering Bootcamp

This is the "consumer" service. It reads sensor data from a shared
file that the "producer" service writes to.

This demonstrates:
  - Two services sharing data via a named volume
  - depends_on (consumer waits for producer to start)
  - Service names as hostnames (not used here, but available)
"""

import json
import os
import sys
import time

# Path to the shared data file (same path as the producer)
DATA_FILE = os.environ.get("DATA_FILE", "/shared/data.json")

print("Consumer starting...")
print(f"Reading sensor data from: {DATA_FILE}")
print("Waiting for producer to write data...")
print()

last_id = 0

while True:
    try:
        with open(DATA_FILE) as f:
            record = json.load(f)

        # Only print if this is a new reading (avoid duplicates)
        if record["id"] != last_id:
            last_id = record["id"]
            print(
                f"[Consumer] Received #{record['id']:04d} — "
                f"temp={record['temperature']}°C, "
                f"humidity={record['humidity']}%"
            )
            sys.stdout.flush()

    except FileNotFoundError:
        # The producer hasn't written the file yet — that's OK
        pass
    except json.JSONDecodeError:
        # The file is being written — partial read, skip this cycle
        pass

    time.sleep(1)
