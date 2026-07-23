# ─────────────────────────────────────────────────────────────────
# 02 — First Python App in Docker
# Analog Data — EdgeAI Engineering Bootcamp
#
# This Dockerfile introduces:
#   - FROM    : choose the base image
#   - WORKDIR : set the working directory inside the container
#   - COPY    : copy files from your computer into the container
#   - ENV     : set environment variables
#   - CMD     : the command to run when the container starts
#
# Build:  docker build -t my-first-app .
# Run:    docker run my-first-app
# Custom: docker run -e NAME=Alice my-first-app
# ─────────────────────────────────────────────────────────────────

# Start from the official Python 3.11 slim image
# 'slim' means it's a smaller version (~150MB instead of ~900MB)
FROM python:3.11-slim

# Set the working directory inside the container
# Think of this like doing 'cd /app' inside the container
# All subsequent COPY, RUN, and CMD commands happen relative to /app
WORKDIR /app

# Copy app.py from your computer (the build context) into the container
# The syntax is: COPY <source_on_host> <destination_in_container>
# '.' means "current directory on host", so COPY app.py . puts it in /app/app.py
COPY app.py .

# Set an environment variable with a default value
# This can be overridden when running the container:
#   docker run -e NAME=Alice my-first-app
ENV NAME="World"

# The command that runs when the container starts
# We run our Python script
CMD ["python3", "app.py"]
