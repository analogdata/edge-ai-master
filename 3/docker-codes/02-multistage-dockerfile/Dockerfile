# ─────────────────────────────────────────────────────────────────
# Multi-Stage Dockerfile for Edge AI Inference Engine
# Analog Data — EdgeAI Engineering Bootcamp (Part 5)
#
# Multi-stage builds produce much smaller images by separating
# the build environment from the runtime environment.
#
# Stage 1 (builder): Large image with gcc, g++ to compile C extensions
# Stage 2 (runtime): Small slim image with only the compiled packages
#
# Image size comparison:
#   Single-stage: 800MB – 1.2GB
#   Multi-stage:  120MB – 200MB
# ─────────────────────────────────────────────────────────────────


# ─────────────────────────────────────────────────────────────────
# STAGE 1: builder
# Large image with all build tools — used ONLY during build
# This stage is discarded after the build is complete
# ─────────────────────────────────────────────────────────────────
FROM python:3.11 AS builder

# Install system-level build dependencies
# These are needed to compile C extensions (like tflite-runtime, numpy)
# --no-install-recommends: skip optional packages to save space
# rm -rf /var/lib/apt/lists/*: clean up apt cache in the SAME layer
#   (combining apt-get install and rm into one RUN with && creates one
#    layer, and the rm actually reduces image size because it's in the
#    same layer as the install)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libatlas-base-dev \
    libhdf5-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory for the build stage
WORKDIR /build

# Copy requirements.txt FIRST — this is the caching trick:
# If requirements.txt hasn't changed, Docker reuses the cached layer
# and skips pip install on the next build. This saves several minutes.
COPY requirements.txt .

# Install Python packages into a separate /install directory
# --prefix=/install: install packages to /install instead of /usr/local
# This makes it easy to copy ONLY the installed packages to the runtime stage
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# ─────────────────────────────────────────────────────────────────
# STAGE 2: runtime
# Small, clean image — this is what actually runs on the Pi
# The builder stage is completely discarded; only copied files remain
# ─────────────────────────────────────────────────────────────────
FROM python:3.11-slim AS runtime

# Install ONLY runtime system libraries (NOT build tools like gcc)
# libatlas3-base: math libraries needed by numpy at runtime
# libgomp1: OpenMP library needed by tflite-runtime at runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
    libatlas3-base \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy compiled Python packages from the builder stage
# This is the key multi-stage command:
#   COPY --from=builder /install /usr/local
# It copies the installed packages from /install (in the builder stage)
# into /usr/local (in the runtime stage, which is on Python's path)
# The builder stage itself is then discarded — it never becomes part
# of the final image.
COPY --from=builder /install /usr/local

# Set the working directory for the application
WORKDIR /app

# Copy the application source code
COPY inference.py .
COPY models/ ./models/

# Set environment variables with sensible defaults
ENV MODEL_PATH=/app/models/model.tflite
ENV LOG_LEVEL=INFO
ENV CONFIDENCE_THRESHOLD=0.75
ENV MQTT_BROKER=localhost
ENV MQTT_PORT=1883
ENV MQTT_TOPIC=sensors/inference

# Document that this app listens on port 8000
EXPOSE 8000

# Run as a non-root user for security
# This is a best practice — if an attacker breaks into the container,
# they have limited permissions (not root)
RUN useradd --create-home appuser
USER appuser

# The command to run when the container starts
CMD ["python3", "inference.py"]
