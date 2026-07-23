#!/usr/bin/env python3
"""
03 — Dockerfile Explained: App Script
Analog Data — EdgeAI Engineering Bootcamp

A simple script that uses every environment variable set in the
annotated Dockerfile. It demonstrates how each Dockerfile instruction
affects the running container.
"""

import os
import platform
import sys

# ─────────────────────────────────────────────────
# Read all environment variables set by the Dockerfile
# ─────────────────────────────────────────────────
app_name = os.environ.get("APP_NAME", "unknown")
version = os.environ.get("VERSION", "0.0.0")
log_level = os.environ.get("LOG_LEVEL", "INFO")
author = os.environ.get("AUTHOR", "unknown")

# ─────────────────────────────────────────────────
# Print information about the container environment
# ─────────────────────────────────────────────────
print("=" * 50)
print(f"  {app_name} v{version}")
print(f"  Author: {author}")
print(f"  Log Level: {log_level}")
print("=" * 50)

# Show the Python version (set by the FROM instruction)
print(f"\nPython version : {sys.version.split()[0]}")

# Show the CPU architecture (important for ARM64 vs x86-64)
print(f"Architecture   : {platform.machine()}")

# Show the working directory (set by WORKDIR)
print(f"Working dir    : {os.getcwd()}")

# Show all environment variables that start with APP or LOG or VERSION
print("\nEnvironment variables from Dockerfile:")
for key in sorted(os.environ):
    if key.startswith(("APP_", "LOG_", "VERSION", "AUTHOR")):
        print(f"  {key} = {os.environ[key]}")

# Show command-line arguments (passed via docker run)
if len(sys.argv) > 1:
    print(f"\nCommand-line arguments: {sys.argv[1:]}")

print("\nContainer is exiting normally.")
