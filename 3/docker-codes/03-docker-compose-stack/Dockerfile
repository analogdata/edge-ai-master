# ─────────────────────────────────────────────────────────────────
# Multi-Stage Dockerfile for Inference Engine
# Analog Data — EdgeAI Engineering Bootcamp (Part 6)
#
# This Dockerfile is used by docker-compose.yml to build the
# inference service. It uses a multi-stage build for a small image.
# ─────────────────────────────────────────────────────────────────

# ─────────────────────────────────────────────────────────────────
# STAGE 1: builder — compile Python packages with build tools
# ─────────────────────────────────────────────────────────────────
FROM python:3.11 AS builder

# Install build dependencies needed to compile C extensions
# Combine apt-get update, install, and cleanup into one RUN to
# create a single layer and actually reduce image size
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libatlas-base-dev \
    libhdf5-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build

# Copy requirements.txt FIRST for layer caching
# If requirements.txt hasn't changed, pip install is skipped on rebuild
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ─────────────────────────────────────────────────────────────────
# STAGE 2: runtime — small clean image that runs on the Pi
# ─────────────────────────────────────────────────────────────────
FROM python:3.11-slim AS runtime

# Install ONLY runtime libraries (not build tools)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libatlas3-base \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy compiled packages from builder stage
COPY --from=builder /install /usr/local

WORKDIR /app

# Copy application code
COPY inference.py .

# Set environment variables (overridden by docker-compose.yml)
ENV MODEL_PATH=/app/models/model.tflite
ENV LOG_LEVEL=INFO
ENV CONFIDENCE_THRESHOLD=0.75
ENV MQTT_BROKER=mqtt
ENV MQTT_PORT=1883
ENV MQTT_TOPIC=sensors/inference

EXPOSE 8000

# Run as non-root user for security
RUN useradd --create-home appuser
USER appuser

CMD ["python3", "inference.py"]
