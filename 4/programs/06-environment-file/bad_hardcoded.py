#!/usr/bin/env python3
"""
06 — BAD: Hardcoded Configuration

This script shows the WRONG way to configure a service.
All values are hardcoded directly in the source code.

Problems:
  1. Push to GitHub → API keys exposed publicly
  2. Deploy to 20 devices with different broker IPs → 20 different script versions
  3. Upgrade model to v3 → edit and re-deploy source code
  4. Change broker IP → edit code, not just config

Compare with good_env_config.py which uses os.environ.get().
"""

# ─────────────────────────────────────────────
# BAD: All values hardcoded in source code
# ─────────────────────────────────────────────
MQTT_BROKER = "192.168.1.100"
API_KEY = "sk_live_abc123verysecretkey"
MODEL_PATH = "/home/pi/models/v2/model.tflite"
CONFIDENCE_THRESHOLD = 0.75
CAMERA_ID = 0
MQTT_PORT = 1883
LOG_LEVEL = "INFO"


def main():
    print("=" * 55)
    print(" BAD: Hardcoded Configuration")
    print("=" * 55)
    print()
    print(" All values are baked into the source code:")
    print()
    print(f"   MQTT_BROKER          = {MQTT_BROKER}")
    print(f"   API_KEY              = {API_KEY}")
    print(f"   MODEL_PATH           = {MODEL_PATH}")
    print(f"   CONFIDENCE_THRESHOLD = {CONFIDENCE_THRESHOLD}")
    print(f"   CAMERA_ID            = {CAMERA_ID}")
    print(f"   MQTT_PORT            = {MQTT_PORT}")
    print(f"   LOG_LEVEL            = {LOG_LEVEL}")
    print()
    print(" Problems with this approach:")
    print()
    print("   1. Push to GitHub → API key 'sk_live_abc...' is PUBLIC")
    print("   2. Deploy to 20 devices → need 20 copies of this script")
    print("   3. Upgrade model to v3 → edit source code + re-deploy")
    print("   4. Change broker IP → edit source code, not just config")
    print()
    print(" Solution: use .env + os.environ.get() (see good_env_config.py)")


if __name__ == "__main__":
    main()
