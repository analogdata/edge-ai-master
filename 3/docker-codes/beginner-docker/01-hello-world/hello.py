#!/usr/bin/env python3
"""
01 — Hello World Python Script
Analog Data — EdgeAI Engineering Bootcamp

The simplest possible Python script to run inside Docker.
Just prints a greeting and exits.

This file is NOT needed for the Dockerfile above (which uses
a Python one-liner directly in CMD). But if you prefer to
copy a script into the container instead, use this version.

To use this script in a Dockerfile instead:
    FROM python:3.11-slim
    WORKDIR /app
    COPY hello.py .
    CMD ["python3", "hello.py"]
"""

print("Hello from Docker!")
print("This message came from a Python script running inside a container.")
