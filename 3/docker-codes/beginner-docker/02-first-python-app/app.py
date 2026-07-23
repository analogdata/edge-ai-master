#!/usr/bin/env python3
"""
02 — First Python App in Docker
Analog Data — EdgeAI Engineering Bootcamp

A simple Python script that:
  - Reads a name from an environment variable (with a default)
  - Prints a personalized greeting
  - Shows the current working directory
  - Lists the files in the working directory

This teaches you how environment variables and the WORKDIR
instruction work inside a Docker container.
"""

import os

# ─────────────────────────────────────────────────
# Read the NAME from an environment variable
# os.environ.get() returns a default value if the variable is not set
# In Docker, you can set this with:
#   - ENV instruction in the Dockerfile
#   - -e flag in docker run:  docker run -e NAME=Alice my-app
#   - environment section in docker-compose.yml
# ─────────────────────────────────────────────────
name = os.environ.get("NAME", "World")

# Print a greeting
print(f"Hello, {name}!")
print("Welcome to your first Dockerized Python app.")

# Show the current working directory
# This is set by the WORKDIR instruction in the Dockerfile
cwd = os.getcwd()
print(f"\nCurrent working directory: {cwd}")

# List files in the current directory
# This shows what COPY . . put into the container
print("\nFiles in this directory:")
for filename in sorted(os.listdir(".")):
    filepath = os.path.join(".", filename)
    if os.path.isfile(filepath):
        size = os.path.getsize(filepath)
        print(f"  {filename}  ({size} bytes)")
    else:
        print(f"  {filename}/  (directory)")

print("\nDone! The container will now exit.")
