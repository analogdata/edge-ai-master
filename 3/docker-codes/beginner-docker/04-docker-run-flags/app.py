#!/usr/bin/env python3
"""
04 — Docker Run Flags: App Script
Analog Data — EdgeAI Engineering Bootcamp

A simple long-running app that prints a counter every 2 seconds.
This is used to demonstrate various `docker run` flags like:
  - -d (detached mode)
  - --name (give the container a name)
  - -e (environment variables)
  - -p (port mapping)
  - --rm (auto-remove when stopped)
  - -v (volume mount)

Run it and try the different docker run commands from the README.
"""

import os
import signal
import sys
import time

# Read configuration from environment variables
app_name = os.environ.get("APP_NAME", "counter-app")
interval = float(os.environ.get("INTERVAL", "2"))

# Graceful shutdown — allows `docker stop` to work cleanly
running = True


def handle_shutdown(signum, frame):
    """Handle SIGTERM (docker stop) or SIGINT (Ctrl+C)."""
    global running
    print(f"\n[{app_name}] Shutdown signal received. Stopping...")
    running = False


signal.signal(signal.SIGTERM, handle_shutdown)
signal.signal(signal.SIGINT, handle_shutdown)

print(f"[{app_name}] Starting...")
print(f"[{app_name}] Interval: {interval}s")
print(f"[{app_name}] Press Ctrl+C or run 'docker stop' to stop.")
print(f"[{app_name}] PID: {os.getpid()}")
print()

counter = 0
while running:
    counter += 1
    print(f"[{app_name}] Count: {counter}")
    sys.stdout.flush()  # ensure output appears immediately in docker logs
    time.sleep(interval)

print(f"[{app_name}] Goodbye! Final count: {counter}")
