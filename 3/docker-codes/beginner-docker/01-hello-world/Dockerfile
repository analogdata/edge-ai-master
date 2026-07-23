# ─────────────────────────────────────────────────────────────────
# 01 — Hello World Dockerfile
# Analog Data — EdgeAI Engineering Bootcamp
#
# This is the ABSOLUTE simplest Dockerfile possible.
# It does one thing: prints "Hello from Docker!" and exits.
#
# Think of this as your very first Docker "recipe".
# A Dockerfile is just a list of instructions that Docker reads
# from top to bottom to build an image.
#
# How to use this:
#   1. Build the image:   docker build -t my-hello .
#   2. Run the container:  docker run my-hello
#
# You should see:  "Hello from Docker!"
# ─────────────────────────────────────────────────────────────────

# FROM — Every Dockerfile starts with FROM.
# This tells Docker "start with this base image".
# 'python:3.11-slim' is a small Python image (~150MB).
# It includes Python 3.11 and nothing else extra.
# This image works on both x86-64 (laptops) and ARM64 (Raspberry Pi).
FROM python:3.11-slim

# CMD — The command that runs when the container starts.
# Here we just run a Python one-liner that prints a message.
# The syntax ["python3", "-c", "..."] is called "exec form".
# It runs the command directly without a shell (recommended).
CMD ["python3", "-c", "print('Hello from Docker!')"]
