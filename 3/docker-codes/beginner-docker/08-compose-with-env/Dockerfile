# ─────────────────────────────────────────────────────────────────
# 08 — Dockerfile with ENV defaults
# Analog Data — EdgeAI Engineering Bootcamp
#
# This Dockerfile sets DEFAULT environment variables using ENV.
# These can be overridden by:
#   - docker-compose.yml 'environment' section
#   - .env file (loaded automatically by Compose)
#   - docker run -e VAR=value
# ─────────────────────────────────────────────────────────────────

FROM python:3.11-slim

WORKDIR /app

COPY app.py .

# Set DEFAULT environment variables
# These are baked into the image and used unless overridden
ENV APP_NAME="env-demo"
ENV ENVIRONMENT="development"
ENV LOG_LEVEL="INFO"
ENV POLL_INTERVAL="5"
ENV MAX_CONNECTIONS="10"

CMD ["python3", "app.py"]
