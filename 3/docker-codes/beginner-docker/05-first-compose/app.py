#!/usr/bin/env python3
"""
05 — First Docker Compose: App Script
Analog Data — EdgeAI Engineering Bootcamp

A simple app that prints a greeting every 3 seconds.
Used to demonstrate the simplest possible docker-compose.yml.
"""

import os
import sys
import time

# Read the greeting message from an environment variable
# In docker-compose.yml, this is set in the 'environment' section
greeting = os.environ.get("GREETING", "Hello from Docker Compose!")

print(f"Starting app with message: {greeting}")
print("This runs inside a Docker Compose service.")
print()

counter = 0
while True:
    counter += 1
    print(f"[{counter:04d}] {greeting}")
    sys.stdout.flush()  # ensure output appears in `docker compose logs`
    time.sleep(3)
