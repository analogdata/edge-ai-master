# ─────────────────────────────────────────────────────────────────
# Basic Dockerfile for Edge AI Inference Engine
# Analog Data — EdgeAI Engineering Bootcamp (Part 4)
#
# This is a simple, single-stage Dockerfile.
# It works but produces a larger image because it includes
# build tools that are not needed at runtime.
# See 02-multistage-dockerfile/ for a smaller, production-ready image.
# ─────────────────────────────────────────────────────────────────

# Start from the official Python 3.11 slim image (ARM64 compatible)
# 'slim' is a smaller variant that excludes many system packages
FROM python:3.11-slim

# Set the working directory inside the container
# All subsequent commands (COPY, RUN) operate relative to this path
WORKDIR /app

# Copy the requirements file FIRST (before the rest of the code)
# This is the "requirements.txt caching trick":
# Docker builds images in layers. If requirements.txt hasn't changed,
# Docker reuses the cached pip install layer — saving minutes on rebuilds.
COPY requirements.txt .

# Install Python dependencies
# --no-cache-dir: don't save pip cache (saves disk space in the image)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
# This happens AFTER pip install so code changes don't trigger reinstalls
COPY . .

# Set environment variables with sensible defaults
# These can be overridden in docker-compose.yml or docker run -e
ENV MODEL_PATH=/app/models/model.tflite
ENV LOG_LEVEL=INFO
ENV CONFIDENCE_THRESHOLD=0.75
ENV MQTT_BROKER=localhost
ENV MQTT_PORT=1883
ENV MQTT_TOPIC=sensors/inference

# Document that this container listens on port 8000
# This is informational only — it does NOT actually publish the port
# You still need -p 8000:8000 in docker run or ports: in compose
EXPOSE 8000

# The command to run when the container starts
# This is the default entry point — can be overridden with docker run <cmd>
CMD ["python3", "inference.py"]
