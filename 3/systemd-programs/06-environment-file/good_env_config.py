#!/usr/bin/env python3
"""
06 — GOOD: Environment-Based Configuration

This script shows the CORRECT way to configure a service.
All values are read from environment variables with sensible fallback defaults.

When running as a systemd service:
  systemd loads the .env file via EnvironmentFile= and sets env vars
  before running this script. All real values are used.

When running locally (development):
  No .env is loaded by systemd, so the fallback defaults are used.
  You can also set env vars manually for testing:
    export MQTT_BROKER=10.0.0.5
    python3 good_env_config.py
"""

import os

# ─────────────────────────────────────────────
# GOOD: Read from environment with fallbacks
# ─────────────────────────────────────────────
MODEL_PATH   = os.environ.get("MODEL_PATH", "/home/pi/edgeai/models/model.tflite")
CAMERA_ID    = int(os.environ.get("CAMERA_ID", "0"))
CONFIDENCE   = float(os.environ.get("CONFIDENCE_THRESHOLD", "0.5"))
MQTT_BROKER  = os.environ.get("MQTT_BROKER", "localhost")
MQTT_PORT    = int(os.environ.get("MQTT_PORT", "1883"))
MQTT_TOPIC   = os.environ.get("MQTT_TOPIC", "sensors/frames")
API_KEY      = os.environ.get("API_KEY", "")
API_ENDPOINT = os.environ.get("API_ENDPOINT", "https://api.example.com/infer")
LOG_LEVEL    = os.environ.get("LOG_LEVEL", "INFO")


def main():
    print("=" * 55)
    print(" GOOD: Environment-Based Configuration")
    print("=" * 55)
    print()
    print(" Values read from os.environ.get() with fallbacks:")
    print()
    print(f"   MODEL_PATH           = {MODEL_PATH}")
    print(f"   CAMERA_ID            = {CAMERA_ID}")
    print(f"   CONFIDENCE_THRESHOLD = {CONFIDENCE}")
    print(f"   MQTT_BROKER          = {MQTT_BROKER}")
    print(f"   MQTT_PORT            = {MQTT_PORT}")
    print(f"   MQTT_TOPIC           = {MQTT_TOPIC}")
    print(f"   API_KEY              = {'***set***' if API_KEY else '(empty - using fallback)'}")
    print(f"   API_ENDPOINT         = {API_ENDPOINT}")
    print(f"   LOG_LEVEL            = {LOG_LEVEL}")
    print()
    print(" How os.environ.get('KEY', 'default') works:")
    print("   1. Look for environment variable named KEY")
    print("   2. If found  → use that value")
    print("   3. If NOT found → use the 'default' fallback")
    print()
    print(" Try setting an env var before running:")
    print("   export MQTT_BROKER=10.0.0.5")
    print("   python3 good_env_config.py")
    print()
    print(" Or load from .env file manually:")
    print("   set -a; source .env.example; set +a")
    print("   python3 good_env_config.py")


if __name__ == "__main__":
    main()
