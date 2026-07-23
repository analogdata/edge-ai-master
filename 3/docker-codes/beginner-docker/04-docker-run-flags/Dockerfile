# ─────────────────────────────────────────────────────────────────
# 04 — Docker Run Flags
# Analog Data — EdgeAI Engineering Bootcamp
#
# A simple app that counts forever, used to demonstrate
# different `docker run` flags.
#
# Build:  docker build -t counter-app .
# ─────────────────────────────────────────────────────────────────

FROM python:3.11-slim

WORKDIR /app

COPY app.py .

ENV APP_NAME="counter-app"
ENV INTERVAL="2"

# No EXPOSE here — this app doesn't listen on any port
# It just prints to stdout

CMD ["python3", "app.py"]
