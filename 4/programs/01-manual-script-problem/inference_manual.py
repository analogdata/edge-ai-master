#!/usr/bin/env python3
"""
01 — Manual Script (The Problem)

This script simulates an Edge AI inference loop running in the foreground.
It demonstrates the core problem: when you close the terminal or press Ctrl+C,
the script dies immediately with no auto-restart.

Run it:
    python3 inference_manual.py

Then try:
    1. Press Ctrl+C         → script dies, no restart
    2. Close the terminal    → script dies, no restart
    3. Kill the process      → script stays dead forever

This is WHY we need systemd (covered in the next programs).
"""

import time
import sys


def main():
    print("=" * 50)
    print(" Edge AI Inference — MANUAL MODE (no systemd)")
    print("=" * 50)
    print()
    print(" This script runs in the foreground.")
    print(" If you close this terminal, the script DIES.")
    print(" If the Pi reboots, the script never starts again.")
    print(" If it crashes, it stays dead until you fix it manually.")
    print()
    print(" Press Ctrl+C to stop (and see how it just dies).")
    print("-" * 50)

    frame_count = 0
    try:
        while True:
            frame_count += 1
            print(f"[Frame {frame_count:06d}] Running inference...")
            time.sleep(5)
    except KeyboardInterrupt:
        print()
        print(" Script killed by Ctrl+C.")
        print(" No auto-restart. No cleanup. No logging.")
        print(" This is the problem systemd solves.")
        sys.exit(0)


if __name__ == "__main__":
    main()
