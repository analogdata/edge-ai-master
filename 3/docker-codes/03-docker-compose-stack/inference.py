#!/usr/bin/env python3
"""
Edge AI Inference Engine — Docker Compose Stack Version
Analog Data — EdgeAI Engineering Bootcamp (Part 6)

This version is designed to run as part of a Docker Compose stack
with 4 services: MQTT broker, inference engine, FastAPI server,
and SQLite backup.

Key difference from the standalone version:
  - MQTT_BROKER is set to "mqtt" (the Docker Compose service name)
    Docker's internal DNS resolves this to the correct container IP.
    You never need to hardcode IP addresses.
"""

import json
import logging
import os
import signal
import sys
import time

import paho.mqtt.client as mqtt

# ─────────────────────────────────────────────────
# Read configuration from environment variables
# In Docker Compose, these are set in the 'environment' section
# of the docker-compose.yml file
# ─────────────────────────────────────────────────
MODEL_PATH = os.environ.get("MODEL_PATH", "/app/models/model.tflite")
MQTT_BROKER = os.environ.get("MQTT_BROKER", "mqtt")  # "mqtt" is the service name
MQTT_PORT = int(os.environ.get("MQTT_PORT", "1883"))
MQTT_TOPIC = os.environ.get("MQTT_TOPIC", "sensors/inference")
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
CONFIDENCE_THRESHOLD = float(os.environ.get("CONFIDENCE_THRESHOLD", "0.75"))

# ─────────────────────────────────────────────────
# Set up logging — output to stdout for `docker compose logs`
# ─────────────────────────────────────────────────
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("edgeai-inference")


# ─────────────────────────────────────────────────
# Graceful shutdown handler
# ─────────────────────────────────────────────────
def handle_shutdown(signum, frame):
    """Handle SIGTERM (docker stop) or SIGINT (Ctrl+C)."""
    log.info("Shutdown signal received. Cleaning up...")
    if "mqtt_client" in globals():
        mqtt_client.disconnect()
    log.info("Cleanup complete. Goodbye.")
    sys.exit(0)


signal.signal(signal.SIGTERM, handle_shutdown)
signal.signal(signal.SIGINT, handle_shutdown)


# ─────────────────────────────────────────────────
# MQTT callbacks
# ─────────────────────────────────────────────────
def on_connect(client, userdata, flags, reason_code, properties):
    """Called when connected to the MQTT broker."""
    if reason_code == 0:
        log.info(f"Connected to MQTT broker at {MQTT_BROKER}:{MQTT_PORT}")
    else:
        log.error(f"Failed to connect. Reason code: {reason_code}")


def on_disconnect(client, userdata, flags, reason_code, properties):
    """Called when disconnected from the MQTT broker."""
    log.info(f"Disconnected from MQTT broker. Reason code: {reason_code}")


# ─────────────────────────────────────────────────
# Simulated inference
# ─────────────────────────────────────────────────
def simulate_inference(frame_count):
    """
    Simulate running inference on a single frame.

    Replace this with real TFLite inference in production:
      from tflite_runtime.interpreter import Interpreter
      interpreter = Interpreter(model_path=MODEL_PATH)
      interpreter.allocate_tensors()
      ...
    """
    result = {
        "frame": frame_count,
        "label": "person",
        "confidence": 0.92,
        "timestamp": time.time(),
    }

    if result["confidence"] >= CONFIDENCE_THRESHOLD:
        log.info(
            f"Frame {frame_count:06d} — detected '{result['label']}' "
            f"with confidence {result['confidence']:.2f}"
        )
        return result
    else:
        log.debug(f"Frame {frame_count:06d} — below threshold, skipping")
        return None


# ─────────────────────────────────────────────────
# Main function
# ─────────────────────────────────────────────────
def main():
    """Set up MQTT connection and run the inference loop."""
    log.info("=" * 50)
    log.info(" Edge AI Inference Engine (Compose Stack) — Starting")
    log.info("=" * 50)
    log.info(f"Model path       : {MODEL_PATH}")
    log.info(f"MQTT broker      : {MQTT_BROKER}:{MQTT_PORT}")
    log.info(f"MQTT topic       : {MQTT_TOPIC}")
    log.info(f"Confidence thresh: {CONFIDENCE_THRESHOLD}")

    # Check for model file
    if not os.path.isfile(MODEL_PATH):
        log.warning(f"Model file not found at {MODEL_PATH} — running in simulation mode")

    # Set up MQTT client
    global mqtt_client
    mqtt_client = mqtt.Client(
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
        client_id="edgeai-inference",
    )
    mqtt_client.on_connect = on_connect
    mqtt_client.on_disconnect = on_disconnect

    try:
        mqtt_client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
        mqtt_client.loop_start()
    except Exception as e:
        log.error(f"Could not connect to MQTT broker: {e}")
        time.sleep(5)

    # Inference loop
    frame_count = 0
    log.info("Starting inference loop...")

    while True:
        frame_count += 1
        result = simulate_inference(frame_count)

        if result is not None:
            payload = json.dumps(result)
            mqtt_client.publish(MQTT_TOPIC, payload)
            log.info(f"Published result to MQTT topic: {MQTT_TOPIC}")

        time.sleep(5)


if __name__ == "__main__":
    main()
