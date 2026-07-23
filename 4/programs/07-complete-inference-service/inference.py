#!/usr/bin/env python3
"""
Edge AI Inference Service
Analog Data — EdgeAI Engineering Bootcamp

Designed to run as a systemd service. Reads all config from
environment variables loaded from .env by systemd.

When running as a service:
  systemd loads .env via EnvironmentFile= and sets env vars
  before running this script.

When running locally:
  Fallback defaults keep the script working for development.
"""

import os
import sys
import time
import signal
import logging

# ─────────────────────────────────────────────────
# Load configuration from environment
# ─────────────────────────────────────────────────
MODEL_PATH   = os.environ.get("MODEL_PATH", "/home/pi/edgeai/models/model.tflite")
CAMERA_ID    = int(os.environ.get("CAMERA_ID", "0"))
CONFIDENCE   = float(os.environ.get("CONFIDENCE_THRESHOLD", "0.5"))
MQTT_BROKER  = os.environ.get("MQTT_BROKER", "localhost")
MQTT_PORT    = int(os.environ.get("MQTT_PORT", "1883"))
MQTT_TOPIC   = os.environ.get("MQTT_TOPIC", "sensors/frames")
API_KEY      = os.environ.get("API_KEY", "")
API_ENDPOINT = os.environ.get("API_ENDPOINT", "https://api.example.com/infer")
LOG_LEVEL    = os.environ.get("LOG_LEVEL", "INFO")

# ─────────────────────────────────────────────────
# Set up logging
# ─────────────────────────────────────────────────
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("edgeai")

# ─────────────────────────────────────────────────
# Graceful shutdown handler
# ─────────────────────────────────────────────────
# systemd sends SIGTERM when you run: systemctl stop edgeai
# We catch it here so the script can clean up before exiting.
def handle_shutdown(signum, frame):
    log.info("Shutdown signal received (SIGTERM). Stopping gracefully...")
    # close camera, MQTT client, file handles etc. here
    log.info("Cleanup complete. Goodbye.")
    sys.exit(0)


signal.signal(signal.SIGTERM, handle_shutdown)
signal.signal(signal.SIGINT, handle_shutdown)   # also handles Ctrl+C during dev

# ─────────────────────────────────────────────────
# Startup checks
# ─────────────────────────────────────────────────
def run_startup_checks():
    log.info("Running startup checks...")
    if not os.path.isfile(MODEL_PATH):
        log.critical(f"Model file not found: {MODEL_PATH}")
        log.critical("Cannot start without model. Exiting.")
        sys.exit(1)   # non-zero exit code triggers Restart=always
    log.info(f"Model found       : {MODEL_PATH}")
    log.info(f"Camera ID         : {CAMERA_ID}")
    log.info(f"Confidence thresh : {CONFIDENCE}")
    log.info(f"MQTT broker       : {MQTT_BROKER}:{MQTT_PORT}")
    log.info(f"MQTT topic        : {MQTT_TOPIC}")
    log.info(f"API endpoint      : {API_ENDPOINT}")
    log.info(f"API key set       : {'yes' if API_KEY else 'no (empty)'}")
    log.info("All checks passed. Starting inference loop.")


# ─────────────────────────────────────────────────
# Main inference loop
# ─────────────────────────────────────────────────
def inference_loop():
    frame_count = 0
    while True:
        frame_count += 1
        # Replace this block with real camera read + model inference
        log.info(f"Frame {frame_count:06d} — running inference...")
        time.sleep(5)   # simulates inference every 5 seconds


# ─────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────
if __name__ == "__main__":
    log.info("=" * 50)
    log.info(" Edge AI Inference Service — Starting")
    log.info("=" * 50)
    run_startup_checks()
    inference_loop()
