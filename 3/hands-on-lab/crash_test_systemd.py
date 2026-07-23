#!/usr/bin/env python3
"""
Crash Test Script for systemd Service
Analog Data — EdgeAI Engineering Bootcamp (Hands-on Lab, Part B)

This script performs the crash test from the lab:
  1. Finds the PID of the running edgeai service
  2. Sends SIGKILL (kill -9) to force-kill it
  3. Times how long systemd takes to restart it
  4. Reports the result

Run this on the Raspberry Pi:
  python3 crash_test_systemd.py

Expected: restart in <= 5 seconds (RestartSec=5 in edgeai.service)
"""

import subprocess
import sys
import time


def get_service_pid():
    """Get the main PID of the edgeai systemd service."""
    result = subprocess.run(
        ["systemctl", "show", "-p", "MainPID", "edgeai"],
        capture_output=True,
        text=True,
    )
    # Output looks like: MainPID=12345
    pid_str = result.stdout.strip().split("=")[1]
    pid = int(pid_str)
    return pid


def main():
    print("=" * 55)
    print("  systemd Crash Test — Edge AI Inference Service")
    print("=" * 55)

    # Step 1: Check the service is running
    result = subprocess.run(["systemctl", "is-active", "edgeai"], capture_output=True, text=True)
    if result.stdout.strip() != "active":
        print("ERROR: edgeai service is not running. Start it first:")
        print("  sudo systemctl start edgeai")
        sys.exit(1)

    # Step 2: Get the current PID
    pid = get_service_pid()
    if pid == 0:
        print("ERROR: Could not find the service PID.")
        sys.exit(1)

    print(f"  Current PID: {pid}")
    print("  Sending SIGKILL (kill -9)...")
    print()

    # Step 3: Kill the process and start timing
    kill_time = time.time()
    subprocess.run(["sudo", "kill", "-9", str(pid)], check=True)

    print(f"  Killed at: {time.strftime('%H:%M:%S', time.localtime(kill_time))}")
    print("  Waiting for systemd to restart (RestartSec=5)...")

    # Step 4: Poll for the service to come back up
    while True:
        time.sleep(0.5)
        new_pid = get_service_pid()
        if new_pid != 0 and new_pid != pid:
            restart_time = time.time()
            elapsed = restart_time - kill_time
            print()
            print(f"  Restarted at: {time.strftime('%H:%M:%S', time.localtime(restart_time))}")
            print(f"  New PID: {new_pid}")
            print(f"  Time to restart: {elapsed:.1f} seconds")
            print()

            # Check result
            if elapsed <= 5.0:
                print("  RESULT: PASS — Restarted within 5 seconds")
            else:
                print(f"  RESULT: FAIL — Took {elapsed:.1f}s (expected <= 5s)")

            # Verify the service is active
            result = subprocess.run(
                ["systemctl", "is-active", "edgeai"], capture_output=True, text=True
            )
            print(f"  Service status: {result.stdout.strip()}")
            print()
            print("  Check the frame counter restarted from 1:")
            print("    journalctl -u edgeai -n 5")
            break

    print()
    print("  Record your result in the lab sheet:")
    print("    Time from crash to restart: ___ seconds")
    print("    Service status after restart: ___")
    print("    Frame counter restarted from 1: Yes/No")


if __name__ == "__main__":
    main()
