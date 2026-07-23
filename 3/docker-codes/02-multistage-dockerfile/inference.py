#!/usr/bin/env python3
"""
Edge AI Inference Engine — Multi-Stage Version
Analog Data — EdgeAI Engineering Bootcamp (Part 5)

This is the same inference script as the basic version, but it is
designed to run in a multi-stage Docker build image.

The multi-stage Dockerfile:
  Stage 1 (builder): Full Python image with gcc, g++ to compile C extensions
  Stage 2 (runtime): Slim Python image with only the compiled packages

This produces a much smaller image (120-200MB vs 800MB-1.2GB).
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
# These are set by the ENV instructions in the Dockerfile
# and can be overridden in docker-compose.yml
# ─────────────────────────────────────────────────
MODEL_PATH = os.environ.get("MODEL_PATH", "/app/models/model.tflite")
MQTT_BROKER = os.environ.get("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.environ.get("MQTT_PORT", "1883"))
MQTT_TOPIC = os.environ.get("MQTT_TOPIC", "sensors/inference")
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
CONFIDENCE_THRESHOLD = float(os.environ.get("CONFIDENCE_THRESHOLD", "0.75"))

# ─────────────────────────────────────────────────
# Set up logging — output goes to stdout for `docker logs`
# ─────────────────────────────────────────────────
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("edgeai-inference")


# ─────────────────────────────────────────────────
# Graceful shutdown handler
# Docker sends SIGTERM when you run: docker stop <container>
# ─────────────────────────────────────────────────
def handle_shutdown(signum, frame):
    """Handle shutdown signals from Docker (SIGTERM) or Ctrl+C (SIGINT)."""
    log.info("Shutdown signal received. Cleaning up...")
    if "mqtt_client" in globals():
        mqtt_client.disconnect()
    log.info("Cleanup complete. Goodbye.")
    sys.exit(0)


signal.signal(signal.SIGTERM, handle_shutdown)
signal.signal(signal.SIGINT, handle_shutdown)


# ─────────────────────────────────────────────────
# MQTT connection callbacks
# ─────────────────────────────────────────────────
def on_connect(client, userdata, flags, reason_code, properties):
    """Called when the MQTT client successfully connects to the broker."""
    if reason_code == 0:
        log.info(f"Connected to MQTT broker at {MQTT_BROKER}:{MQTT_PORT}")
    else:
        log.error(f"Failed to connect to MQTT broker. Reason code: {reason_code}")


def on_disconnect(client, userdata, flags, reason_code, properties):
    """Called when the MQTT client disconnects from the broker."""
    log.info(f"Disconnected from MQTT broker. Reason code: {reason_code}")


# ─────────────────────────────────────────────────
# Simulated inference function
# In a real app, this would load a TFLite model using tflite_runtime
# ─────────────────────────────────────────────────
def simulate_inference(frame_count):
    """
    Simulate running inference on a single frame.

    In a real deployment with tflite-runtime, this would look like:

        from tflite_runtime.interpreter import Interpreter
        interpreter = Interpreter(model_path=MODEL_PATH)
        interpreter.allocate_tensors()
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()
        # ... set input tensor, invoke, read output tensor ...

    For this beginner example, we return a simulated result.
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
# Main inference loop
# ─────────────────────────────────────────────────
def main():
    """Main entry point — sets up MQTT and runs the inference loop."""
    log.info("=" * 50)
    log.info(" Edge AI Inference Engine (Multi-Stage) — Starting")
    log.info("=" * 50)
    log.info(f"Model path       : {MODEL_PATH}")
    log.info(f"MQTT broker      : {MQTT_BROKER}:{MQTT_PORT}")
    log.info(f"MQTT topic       : {MQTT_TOPIC}")
    log.info(f"Confidence thresh: {CONFIDENCE_THRESHOLD}")

    # Check if model file exists
    if not os.path.isfile(MODEL_PATH):
        log.warning(f"Model file not found at {MODEL_PATH} — running in simulation mode")

    # Set up MQTT client (paho-mqtt v2 API)
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

    # Inference loop — runs forever until Docker stops the container
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
