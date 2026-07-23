# ─────────────────────────────────────────────────────────────────
# 03 — Dockerfile Explained (Every Instruction Annotated)
# Analog Data — EdgeAI Engineering Bootcamp
#
# This Dockerfile demonstrates EVERY common Dockerfile instruction
# with detailed comments explaining what each one does.
#
# Use this as a reference card. You don't need all of these in every
# project — pick the ones you need.
#
# Build:  docker build -t dockerfile-explained .
# Run:    docker run dockerfile-explained
# ─────────────────────────────────────────────────────────────────

# ─────────────────────────────────────────────────────────────────
# FROM — The base image. Every Dockerfile MUST start with FROM.
# This is the starting point — Docker downloads this image and
# adds your instructions on top of it.
#
# Common choices:
#   python:3.11         — full Python image (~900MB), includes everything
#   python:3.11-slim    — slim version (~150MB), minimal extras
#   python:3.11-alpine  — tiny version (~50MB), but harder to use
#   ubuntu:22.04        — just Ubuntu, no Python pre-installed
#
# For Raspberry Pi: all official Python images support ARM64.
# ─────────────────────────────────────────────────────────────────
FROM python:3.11-slim

# ─────────────────────────────────────────────────────────────────
# LABEL — Adds metadata to the image (optional but good practice).
# You can add any key-value pairs. These show up in `docker inspect`.
# ─────────────────────────────────────────────────────────────────
LABEL maintainer="Analog Data <info@analogdata.com>"
LABEL description="Educational Dockerfile explaining every instruction"
LABEL version="1.0"

# ─────────────────────────────────────────────────────────────────
# WORKDIR — Sets the working directory inside the container.
# Like running 'cd /app' before every subsequent command.
# If the directory doesn't exist, Docker creates it automatically.
# All COPY, RUN, and CMD paths are relative to this directory.
# ─────────────────────────────────────────────────────────────────
WORKDIR /app

# ─────────────────────────────────────────────────────────────────
# COPY — Copies files from your computer INTO the container.
# Format: COPY <source_on_host> <destination_in_container>
#
# You can copy a single file:
#   COPY app.py .
# Or multiple files:
#   COPY app.py utils.py .
# Or an entire directory:
#   COPY . .
#
# Tip: Use .dockerignore to exclude files you don't want copied.
# ─────────────────────────────────────────────────────────────────
COPY app.py .

# ─────────────────────────────────────────────────────────────────
# RUN — Runs a shell command DURING the build (not at runtime).
# Each RUN creates a new layer in the image.
#
# Common uses:
#   RUN pip install -r requirements.txt    — install Python packages
#   RUN apt-get update && apt-get install -y gcc  — install system packages
#
# Tip: Combine multiple commands with && to create fewer layers:
#   RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*
#
# This RUN doesn't do much — just creates a marker file so you can
# see that RUN executed during the build.
# ─────────────────────────────────────────────────────────────────
RUN echo "This file was created during the Docker build" > /app/build_marker.txt

# ─────────────────────────────────────────────────────────────────
# ENV — Sets environment variables inside the container.
# These are available both during build (in RUN commands) and at
# runtime (when the container runs).
#
# They can be overridden with:
#   docker run -e APP_NAME="Custom Name" my-image
# ─────────────────────────────────────────────────────────────────
ENV APP_NAME="Dockerfile Explained"
ENV VERSION="1.0"
ENV LOG_LEVEL="INFO"
ENV AUTHOR="Analog Data"

# ─────────────────────────────────────────────────────────────────
# EXPOSE — Documents which port the container listens on.
# This is INFORMATIONAL ONLY — it does NOT actually publish the port.
# You still need -p flag in docker run or ports: in compose.
#
# Example: EXPOSE 8000 means "this app listens on port 8000"
#   docker run -p 8000:8000 my-image  — maps host:8000 to container:8000
# ─────────────────────────────────────────────────────────────────
EXPOSE 8000

# ─────────────────────────────────────────────────────────────────
# USER — Runs the container as a non-root user (security best practice).
# By default, containers run as root (user ID 0).
# Creating a non-root user and switching to it is safer.
#
# If an attacker breaks into your container, they only have the
# permissions of 'appuser', not root.
# ─────────────────────────────────────────────────────────────────
RUN useradd --create-home appuser
USER appuser

# ─────────────────────────────────────────────────────────────────
# CMD — The DEFAULT command that runs when the container starts.
# There can only be ONE CMD per Dockerfile (if multiple, only the
# last one takes effect).
#
# Format: CMD ["executable", "arg1", "arg2"]
# This is called "exec form" and is the recommended way.
#
# You can override CMD at runtime:
#   docker run my-image python3 -c "print('different command')"
# ─────────────────────────────────────────────────────────────────
CMD ["python3", "app.py"]

# ─────────────────────────────────────────────────────────────────
# ENTRYPOINT (not used here, but important to know):
#
# Like CMD, but HARDER to override. The command is always run,
# and any arguments from docker run are APPENDED to it.
#
# Example:
#   ENTRYPOINT ["python3", "app.py"]
#   CMD ["--help"]
#
#   docker run my-image           → runs: python3 app.py --help
#   docker run my-image --verbose → runs: python3 app.py --verbose
#
# Common pattern: ENTRYPOINT for the main executable, CMD for defaults.
# ─────────────────────────────────────────────────────────────────
