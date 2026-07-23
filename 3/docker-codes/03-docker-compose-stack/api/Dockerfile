# ─────────────────────────────────────────────────────────────────
# Dockerfile for the FastAPI Server
# Analog Data — EdgeAI Engineering Bootcamp (Part 6)
#
# This Dockerfile builds the API service that is part of the
# Docker Compose stack. It uses a simple single-stage build since
# the API doesn't need heavy C extensions.
# ─────────────────────────────────────────────────────────────────

FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Set environment variables (overridden by docker-compose.yml)
ENV MQTT_BROKER=mqtt
ENV MQTT_PORT=1883
ENV MQTT_TOPIC=sensors/inference
ENV DB_PATH=/app/db/results.db
ENV LOG_LEVEL=INFO

# Expose the FastAPI port
EXPOSE 8000

# Run as non-root user for security
RUN useradd --create-home appuser
USER appuser

# Start the FastAPI server with uvicorn
# --host 0.0.0.0: listen on all interfaces (not just localhost)
# --port 8000: listen on port 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
