#!/usr/bin/env python3
"""
07 — Compose with Volumes: Persistence App
Analog Data — EdgeAI Engineering Bootcamp

This app demonstrates Docker volumes by:
  1. Reading a counter from a file (if it exists)
  2. Incrementing the counter
  3. Writing it back to the file
  4. Printing the current count

When you restart the container, the counter CONTINUES from where it
left off — because the file is on a Docker volume that persists.

Without a volume, the counter would reset to 0 every time the
container restarts, because containers are ephemeral (temporary).
"""

import os
import sys
import time

# Path to the persistent data file
# This path is inside a Docker volume, so it survives container restarts
DATA_FILE = os.environ.get("DATA_FILE", "/data/counter.txt")


def read_counter():
    """Read the counter from the data file. Returns 0 if file doesn't exist."""
    try:
        with open(DATA_FILE) as f:
            return int(f.read().strip())
    except FileNotFoundError:
        # First run — no file yet
        return 0
    except (ValueError, OSError):
        # File exists but is empty or corrupted
        return 0


def write_counter(value):
    """Write the counter value to the data file."""
    # Ensure the directory exists
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w") as f:
        f.write(str(value))


# ─────────────────────────────────────────────────
# Main loop
# ─────────────────────────────────────────────────
print("=" * 50)
print("  Volume Persistence Demo")
print("=" * 50)
print(f"  Data file: {DATA_FILE}")
print()

# Read the current counter value from the persistent file
counter = read_counter()

if counter == 0:
    print("  First run — starting from 0")
else:
    print(f"  Resuming from previous count: {counter}")
print()

# Increment and save every 3 seconds
while True:
    counter += 1
    write_counter(counter)
    print(f"  Count: {counter}  (saved to volume)")
    sys.stdout.flush()
    time.sleep(3)
