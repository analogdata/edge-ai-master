#!/usr/bin/env python3
"""
Crash Test Script for Docker Container
Analog Data — EdgeAI Engineering Bootcamp (Hands-on Lab, Part C)

This script performs the Docker crash test from the lab:
  1. Checks the container is running
  2. Sends SIGKILL to force-kill it
  3. Times how long Docker takes to restart it
  4. Reports the result

Run this on the Raspberry Pi:
  python3 crash_test_docker.py

Expected: restart in < 5 seconds (Docker's default is usually under 2s)
"""

import subprocess
import sys
import time


def get_container_status():
    """Check if the edgeai_lab container is running."""
    result = subprocess.run(
        ["docker", "inspect", "-f", "{{.State.Status}}", "edgeai_lab"],
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def get_container_pid():
    """Get the PID of the edgeai_lab container's main process."""
    result = subprocess.run(
        ["docker", "inspect", "-f", "{{.State.Pid}}", "edgeai_lab"],
        capture_output=True,
        text=True,
    )
    try:
        return int(result.stdout.strip())
    except ValueError:
        return 0


def main():
    print("=" * 55)
    print("  Docker Crash Test — Edge AI Inference Container")
    print("=" * 55)

    # Step 1: Check the container is running
    status = get_container_status()
    if status != "running":
        print(f"ERROR: edgeai_lab container is not running (status: {status}).")
        print("Start it first:  docker compose up -d")
        sys.exit(1)

    pid = get_container_pid()
    print("  Container: edgeai_lab")
    print(f"  Status:    {status}")
    print(f"  PID:       {pid}")
    print()

    # Step 2: Kill the container and start timing
    print("  Sending SIGKILL (docker kill --signal=SIGKILL)...")
    kill_time = time.time()
    subprocess.run(["docker", "kill", "--signal=SIGKILL", "edgeai_lab"], check=True)

    print(f"  Killed at: {time.strftime('%H:%M:%S', time.localtime(kill_time))}")
    print("  Waiting for Docker to restart (restart: always)...")

    # Step 3: Poll for the container to come back up
    while True:
        time.sleep(0.5)
        status = get_container_status()
        if status == "running":
            restart_time = time.time()
            elapsed = restart_time - kill_time
            new_pid = get_container_pid()

            print()
            print(f"  Restarted at: {time.strftime('%H:%M:%S', time.localtime(restart_time))}")
            print(f"  New PID: {new_pid}")
            print(f"  Time to restart: {elapsed:.1f} seconds")
            print()

            # Check result
            if elapsed < 5.0:
                print(f"  RESULT: PASS — Restarted in {elapsed:.1f}s (< 5s)")
            else:
                print(f"  RESULT: FAIL — Took {elapsed:.1f}s (expected < 5s)")

            print()
            print("  Verify with:")
            print("    docker compose ps")
            print("    docker compose logs -f inference")
            print()
            print("  Record your result in the lab sheet:")
            print("    Time from kill to restart: ___ seconds")
            print("    Container status after restart: Up ___ seconds")
            print("    Frame counter restarted from 1: Yes/No")
            break

        # Safety: don't wait forever
        if time.time() - kill_time > 30:
            print()
            print("  RESULT: FAIL — Container did not restart within 30 seconds")
            print("  Check: docker compose ps")
            print("  Check: docker compose logs inference")
            break


if __name__ == "__main__":
    main()
