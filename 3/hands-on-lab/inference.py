#!/usr/bin/env python3
"""
Lab Inference Script — Module 3 Hands-on Lab
Analog Data EdgeAI Bootcamp

Simulates an Edge AI inference loop.
Designed to work as both a systemd service and a Docker container.

Configuration is read entirely from environment variables so the
same script works in three contexts:
  1. Direct:    python3 inference.py
  2. systemd:   managed by edgeai.service, .env loaded by systemd
  3. Docker:    managed by docker-compose.yml, env vars set in compose

The script checks that the model file exists before starting.
If the model is missing, it exits with a non-zero code — which
triggers an automatic restart in both systemd (Restart=always)
and Docker (restart: always).
"""

import logging
import os
import signal
import sys
import time

# ── Configuration from environment ──────────────────────────
# os.environ.get() reads a variable, falling back to a default
# if the variable is not set. This makes the script flexible:
#   - Running directly? Uses the default paths.
#   - Running under systemd? Reads from .env via EnvironmentFile.
#   - Running in Docker? Reads from docker-compose.yml environment.
MODEL_PATH = os.environ.get("MODEL_PATH", "/home/pi/edgeai/models/model.tflite")
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
INTERVAL = float(os.environ.get("INFERENCE_INTERVAL", "2.0"))

# ── Logging setup ────────────────────────────────────────────
# Logs go to stdout so both journalctl (systemd) and docker logs can capture them.
# The format includes timestamp, log level, and the message.
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("edgeai-lab")


# ── Graceful shutdown ────────────────────────────────────────
# systemd sends SIGTERM when you run: systemctl stop edgeai
# Docker sends SIGTERM when you run: docker stop or docker compose down
# We catch it so the script can exit cleanly instead of being killed mid-loop.
def handle_shutdown(signum, frame):
    """Handle SIGTERM (systemd/Docker stop) or SIGINT (Ctrl+C)."""
    log.info("Shutdown signal received. Exiting cleanly.")
    sys.exit(0)


signal.signal(signal.SIGTERM, handle_shutdown)
signal.signal(signal.SIGINT, handle_shutdown)

# ── Startup ──────────────────────────────────────────────────
log.info("=" * 55)
log.info("  Edge AI Inference Service — LAB VERSION")
log.info("=" * 55)
log.info(f"Model path : {MODEL_PATH}")
log.info(f"Interval   : {INTERVAL}s between frames")

# Check that the model file exists before starting
# If it doesn't, exit with code 1 — this triggers a restart
# in both systemd (Restart=always) and Docker (restart: always)
if not os.path.exists(MODEL_PATH):
    log.critical(f"Model file not found at: {MODEL_PATH}")
    log.critical("Exiting. Fix the path and try again.")
    sys.exit(1)

log.info("Model file found. Starting inference loop.")

# ── Main loop ────────────────────────────────────────────────
# Runs forever, simulating inference on each frame.
# In a real app, each iteration would:
#   1. Capture a frame from the camera
#   2. Preprocess the input
#   3. Run the TFLite model
#   4. Post-process and publish the result
frame_count = 0
start_time = time.time()

while True:
    frame_count += 1
    elapsed = time.time() - start_time
    fps = frame_count / elapsed if elapsed > 0 else 0

    log.info(f"Frame {frame_count:06d} | Elapsed: {elapsed:.1f}s | Avg FPS: {fps:.2f}")

    # Simulate inference work (replace with real model inference)
    time.sleep(INTERVAL)
