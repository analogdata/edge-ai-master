#!/usr/bin/env python3
"""
Edge AI Inference Engine — Basic Version
Analog Data — EdgeAI Engineering Bootcamp

This is a beginner-friendly inference script that:
  1. Reads configuration from environment variables
  2. Connects to an MQTT broker
  3. Simulates running inference on sensor data
  4. Publishes results to an MQTT topic

In a real deployment, you would replace the simulate_inference()
function with actual TFLite model inference code.

This script is designed to run inside a Docker container.
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
# Docker sets these via the ENV instruction in the Dockerfile
# or via the environment section in docker-compose.yml
# ─────────────────────────────────────────────────
MODEL_PATH = os.environ.get("MODEL_PATH", "/app/models/model.tflite")
MQTT_BROKER = os.environ.get("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.environ.get("MQTT_PORT", "1883"))
MQTT_TOPIC = os.environ.get("MQTT_TOPIC", "sensors/inference")
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
CONFIDENCE_THRESHOLD = float(os.environ.get("CONFIDENCE_THRESHOLD", "0.75"))

# ─────────────────────────────────────────────────
# Set up logging
# Logs go to stdout so `docker logs` can capture them
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
# We catch it so the script can disconnect from MQTT cleanly
# ─────────────────────────────────────────────────
def handle_shutdown(signum, frame):
    """Handle shutdown signals from Docker (SIGTERM) or Ctrl+C (SIGINT)."""
    log.info("Shutdown signal received. Cleaning up...")
    log.info("Disconnecting from MQTT broker...")
    # The MQTT client is defined later, we use a global to access it here
    if "mqtt_client" in globals():
        mqtt_client.disconnect()
    log.info("Cleanup complete. Goodbye.")
    sys.exit(0)


signal.signal(signal.SIGTERM, handle_shutdown)
signal.signal(signal.SIGINT, handle_shutdown)


# ─────────────────────────────────────────────────
# MQTT connection callbacks
# These are called automatically by paho-mqtt when events happen
# ─────────────────────────────────────────────────
def on_connect(client, userdata, flags, reason_code, properties):
    """Called when the MQTT client connects to the broker."""
    if reason_code == 0:
        log.info(f"Connected to MQTT broker at {MQTT_BROKER}:{MQTT_PORT}")
    else:
        log.error(f"Failed to connect to MQTT broker. Reason code: {reason_code}")


def on_disconnect(client, userdata, flags, reason_code, properties):
    """Called when the MQTT client disconnects from the broker."""
    log.info(f"Disconnected from MQTT broker. Reason code: {reason_code}")


# ─────────────────────────────────────────────────
# Simulated inference function
# In a real app, this would load a TFLite model and run inference
# ─────────────────────────────────────────────────
def simulate_inference(frame_count):
    """
    Simulate running inference on a single frame.

    In a real deployment, this function would:
      1. Capture a frame from the camera (or read sensor data)
      2. Preprocess the input (resize, normalize)
      3. Run the TFLite model: interpreter.invoke()
      4. Post-process the output (apply confidence threshold)

    For this beginner example, we return a simulated result.
    """
    # Simulated inference result — replace with real model output
    result = {
        "frame": frame_count,
        "label": "person",
        "confidence": 0.92,  # simulated confidence score
        "timestamp": time.time(),
    }

    # Only publish if confidence meets the threshold
    if result["confidence"] >= CONFIDENCE_THRESHOLD:
        log.info(
            f"Frame {frame_count:06d} — detected '{result['label']}' "
            f"with confidence {result['confidence']:.2f} (threshold: {CONFIDENCE_THRESHOLD})"
        )
        return result
    else:
        log.debug(
            f"Frame {frame_count:06d} — confidence {result['confidence']:.2f} "
            f"below threshold {CONFIDENCE_THRESHOLD}, skipping"
        )
        return None


# ─────────────────────────────────────────────────
# Main inference loop
# ─────────────────────────────────────────────────
def main():
    """Main entry point — sets up MQTT and runs the inference loop."""
    log.info("=" * 50)
    log.info(" Edge AI Inference Engine — Starting")
    log.info("=" * 50)
    log.info(f"Model path       : {MODEL_PATH}")
    log.info(f"MQTT broker      : {MQTT_BROKER}:{MQTT_PORT}")
    log.info(f"MQTT topic       : {MQTT_TOPIC}")
    log.info(f"Confidence thresh: {CONFIDENCE_THRESHOLD}")
    log.info(f"Log level        : {LOG_LEVEL}")

    # Check if model file exists (optional — in production this is critical)
    if not os.path.isfile(MODEL_PATH):
        log.warning(f"Model file not found at {MODEL_PATH} — running in simulation mode")

    # ─────────────────────────────────────────────────
    # Set up MQTT client
    # paho-mqtt v2 uses a CallbackAPIVersion parameter
    # ─────────────────────────────────────────────────
    global mqtt_client
    mqtt_client = mqtt.Client(
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
        client_id="edgeai-inference",
    )
    mqtt_client.on_connect = on_connect
    mqtt_client.on_disconnect = on_disconnect

    # Connect to the MQTT broker
    # In Docker Compose, the broker hostname is the service name (e.g., "mqtt")
    try:
        mqtt_client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
        mqtt_client.loop_start()  # runs MQTT network loop in a background thread
    except Exception as e:
        log.error(f"Could not connect to MQTT broker: {e}")
        log.error("Retrying in 5 seconds...")
        time.sleep(5)

    # ─────────────────────────────────────────────────
    # Inference loop — runs forever until stopped
    # ─────────────────────────────────────────────────
    frame_count = 0
    log.info("Starting inference loop...")

    while True:
        frame_count += 1

        # Run inference (simulated for this example)
        result = simulate_inference(frame_count)

        # If we got a valid result, publish it to MQTT
        if result is not None:
            # Convert the result dict to a JSON string and publish
            payload = json.dumps(result)
            mqtt_client.publish(MQTT_TOPIC, payload)
            log.info(f"Published result to MQTT topic: {MQTT_TOPIC}")

        # Wait before processing the next frame
        # In a real app, this would be tied to the camera frame rate
        time.sleep(5)


# ─────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────
if __name__ == "__main__":
    main()
