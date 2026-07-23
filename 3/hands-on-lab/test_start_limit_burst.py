#!/usr/bin/env python3
"""
Extension Task 3 — Test StartLimitBurst
Analog Data — EdgeAI Engineering Bootcamp (Hands-on Lab, Extension)

This script demonstrates the StartLimitBurst / StartLimitIntervalSec
mechanism in systemd:

  1. Temporarily patches inference.py to crash immediately (sys.exit(1))
  2. Restarts the systemd service
  3. Watches systemd retry and eventually give up
  4. Reports what systemctl status shows

The service file has:
  StartLimitIntervalSec=60  — within a 60-second window
  StartLimitBurst=5         — allow at most 5 restart attempts

After 5 rapid crashes within 60 seconds, systemd stops retrying
and marks the service as "failed".

Run this on the Raspberry Pi:
  python3 test_start_limit_burst.py

NOTE: This script modifies inference.py temporarily and restores it
after the test. Make sure you have a backup or git commit.
"""

import os
import subprocess
import sys
import time

# Path to the inference script
SCRIPT_PATH = os.path.join(os.path.dirname(__file__), "inference.py")
BACKUP_PATH = SCRIPT_PATH + ".bak"


def backup_script():
    """Back up the original inference.py."""
    import shutil

    shutil.copy2(SCRIPT_PATH, BACKUP_PATH)
    print(f"  Backed up inference.py to {BACKUP_PATH}")


def patch_script_to_crash():
    """Add sys.exit(1) at the top of the main loop to force immediate crash."""
    with open(SCRIPT_PATH) as f:
        content = f.read()

    # Insert sys.exit(1) right before the main loop
    patched = content.replace(
        "# ── Main loop",
        "sys.exit(1)  # FORCED CRASH — test_start_limit_burst.py\n\n# ── Main loop",
    )

    with open(SCRIPT_PATH, "w") as f:
        f.write(patched)

    print("  Patched inference.py to crash immediately (sys.exit(1))")


def restore_script():
    """Restore the original inference.py from backup."""
    import shutil

    if os.path.exists(BACKUP_PATH):
        shutil.move(BACKUP_PATH, SCRIPT_PATH)
        print("  Restored original inference.py")
    else:
        print("  WARNING: Backup not found — inference.py may still be patched!")


def main():
    print("=" * 55)
    print("  Extension Task 3 — Test StartLimitBurst")
    print("=" * 55)
    print()
    print("  This test will:")
    print("    1. Patch inference.py to crash immediately")
    print("    2. Restart the systemd service")
    print("    3. Watch systemd retry up to 5 times (StartLimitBurst=5)")
    print("    4. Observe systemd give up and mark the service as 'failed'")
    print()

    # Check the service exists
    result = subprocess.run(["systemctl", "is-enabled", "edgeai"], capture_output=True, text=True)
    if result.returncode != 0:
        print("  ERROR: edgeai service not found. Install it first.")
        sys.exit(1)

    try:
        # Step 1: Backup and patch
        print("  Step 1: Backing up and patching inference.py...")
        backup_script()
        patch_script_to_crash()

        # Step 2: Reset failure count and restart
        print()
        print("  Step 2: Resetting failure count and restarting service...")
        subprocess.run(["sudo", "systemctl", "reset-failed", "edgeai"])
        subprocess.run(["sudo", "systemctl", "restart", "edgeai"])

        # Step 3: Watch the restart attempts
        print()
        print("  Step 3: Watching restart attempts (up to 60 seconds)...")
        print("  Each restart attempt has RestartSec=5, so 5 attempts = ~25s")
        print()

        start = time.time()
        while time.time() - start < 70:
            result = subprocess.run(
                ["systemctl", "is-active", "edgeai"], capture_output=True, text=True
            )
            status = result.stdout.strip()
            elapsed = time.time() - start

            # Check the restart count
            show_result = subprocess.run(
                ["systemctl", "show", "-p", "NRestarts", "edgeai"],
                capture_output=True,
                text=True,
            )
            restarts = show_result.stdout.strip().split("=")[1] if show_result.stdout else "?"

            print(f"  [{elapsed:5.1f}s] status={status:12s}  NRestarts={restarts}")

            if status == "failed":
                print()
                print("  Service marked as FAILED — systemd gave up!")
                print(f"  Total time: {elapsed:.1f}s")
                break

            time.sleep(3)

        # Step 4: Show the final status
        print()
        print("  Step 4: Final systemctl status:")
        print()
        result = subprocess.run(["systemctl", "status", "edgeai"], capture_output=True, text=True)
        # Print the first 15 lines of status output
        for line in result.stdout.split("\n")[:15]:
            print(f"    {line}")
        print()

    finally:
        # Always restore the original script
        print()
        print("  Cleaning up: restoring original inference.py...")
        restore_script()

        # Reset the service
        subprocess.run(["sudo", "systemctl", "reset-failed", "edgeai"])
        subprocess.run(["sudo", "systemctl", "restart", "edgeai"])
        print("  Service restarted with the original (working) script.")

    print()
    print("  What you should have observed:")
    print("    - systemd retried the service up to 5 times")
    print("    - Each retry was ~5 seconds apart (RestartSec=5)")
    print("    - After 5 failures in 60s, systemd stopped (StartLimitBurst=5)")
    print("    - systemctl status showed 'failed' with a message about")
    print("      start-limit-hit")


if __name__ == "__main__":
    main()
