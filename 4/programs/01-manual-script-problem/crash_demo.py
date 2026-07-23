#!/usr/bin/env python3
"""
01b — Simulated Crash

This script deliberately crashes after a few iterations to show that
a manually-run script stays dead after crashing — no auto-restart.
"""

import time


def main():
    print(" Simulating an inference loop that will crash...")
    print(" Watch what happens when it crashes — nothing. It just dies.")
    print()

    for i in range(1, 6):
        print(f"[Frame {i:06d}] Running inference...")
        time.sleep(2)

    print()
    print(" !!! Simulating a crash (division by zero) !!!")
    result = 1 / 0  # deliberate crash
    print(f"This line never runs: {result}")


if __name__ == "__main__":
    main()
