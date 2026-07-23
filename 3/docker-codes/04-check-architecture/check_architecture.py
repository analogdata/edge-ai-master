#!/usr/bin/env python3
"""
Check Architecture Inside a Container
Analog Data — EdgeAI Engineering Bootcamp (Part 9)

This script checks the CPU architecture of the machine it runs on.
It is useful for verifying that you are running on ARM64 (aarch64)
when working with a Raspberry Pi.

You can run this script:
  1. Directly on your Pi:   python3 check_architecture.py
  2. Inside a container:    docker run --rm python:3.11-slim python3 check_architecture.py

The Raspberry Pi uses an ARM64 processor (aarch64).
Most desktop computers use x86-64 (amd64).
A Docker image built for x86-64 will NOT run on a Raspberry Pi.
"""

import platform
import sys


def check_architecture():
    """
    Detect and display the CPU architecture.

    Common values:
      aarch64 / arm64 — Raspberry Pi 4B/5 (ARM 64-bit)
      x86_64  / amd64 — Most desktop/laptop computers (Intel/AMD 64-bit)
      armv7l          — Older Raspberry Pi models (ARM 32-bit)
    """
    # Get the machine hardware name (e.g., 'aarch64', 'x86_64', 'armv7l')
    machine = platform.machine()

    # Get a human-readable description of the system
    system = platform.system()
    processor = platform.processor()

    print("=" * 50)
    print(" Architecture Check")
    print("=" * 50)
    print(f"  System    : {system}")
    print(f"  Machine   : {machine}")
    print(f"  Processor : {processor or '(not reported)'}")
    print("=" * 50)

    # Check if this is an ARM64 architecture
    # Different OSes may report ARM64 differently
    arm64_names = {"aarch64", "arm64"}
    x86_names = {"x86_64", "amd64", "x86-64"}

    if machine.lower() in arm64_names:
        print("  Result: ARM64 (aarch64) detected")
        print("  This is a Raspberry Pi or other ARM64 device.")
        print("  Docker images must be ARM64-compatible.")
        return 0
    elif machine.lower() in x86_names:
        print("  Result: x86-64 (amd64) detected")
        print("  This is a standard Intel/AMD computer.")
        print("  ARM64 Docker images will NOT run here without emulation.")
        return 0
    else:
        print(f"  Result: Unknown architecture '{machine}'")
        print("  Check Docker Hub for compatible images.")
        return 1


if __name__ == "__main__":
    sys.exit(check_architecture())
