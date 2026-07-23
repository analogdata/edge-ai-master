# ─────────────────────────────────────────────────────────────────
# Multi-Stage Dockerfile — Lab Inference Script
# Analog Data — EdgeAI Engineering Bootcamp (Hands-on Lab, Part C)
#
# Two stages:
#   1. builder  — full Python image with build tools (for compiling packages)
#   2. runtime  — slim Python image with only the compiled packages
#
# Build:  docker compose build
# Run:    docker compose up -d
# ─────────────────────────────────────────────────────────────────

# ─────────────────────────────────────────────────────────────────
# STAGE 1: builder
# Install any packages that need compilation (gcc, g++ for C extensions)
# For the lab, we have no external packages, but the structure is here
# for when you add tflite-runtime, numpy, etc.
# ─────────────────────────────────────────────────────────────────
FROM python:3.11 AS builder

# Install build dependencies (needed for compiling C extensions)
# Combining into one RUN with && creates one layer and reduces image size
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory for the build stage
WORKDIR /build

# Copy requirements and install to a prefix directory
# --prefix=/install: install packages to /install instead of /usr/local
# This makes it easy to copy ONLY the installed packages to the runtime stage
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ─────────────────────────────────────────────────────────────────
# STAGE 2: runtime
# Small, clean image — only what is needed to run the app
# The builder stage is completely discarded after the build
# ─────────────────────────────────────────────────────────────────
FROM python:3.11-slim AS runtime

# Copy installed packages from the builder stage
# This is the key multi-stage command: copies compiled packages
# from /install (builder) to /usr/local (runtime, on Python's path)
COPY --from=builder /install /usr/local

# Set working directory
WORKDIR /app

# Copy the application source code
COPY inference.py .

# Create the models directory inside the container
# The model file is mounted at runtime via docker-compose.yml volumes
RUN mkdir -p /app/models

# Set environment variable defaults
# These can be overridden by docker-compose.yml or docker run -e
ENV MODEL_PATH=/app/models/model.tflite
ENV LOG_LEVEL=INFO
ENV INFERENCE_INTERVAL=2.0

# Run as a non-root user for security
# Create 'appuser' and give it ownership of /app
RUN useradd --create-home appuser && chown -R appuser /app
USER appuser

# Start the inference app
CMD ["python3", "inference.py"]
