#!/usr/bin/env python3
"""
08 — Compose with Environment Variables
Analog Data — EdgeAI Engineering Bootcamp

This app reads ALL its configuration from environment variables.
It demonstrates three ways to pass environment variables in Docker:

  1. ENV in Dockerfile       → defaults baked into the image
  2. environment in compose  → overrides at runtime
  3. .env file               → secrets loaded automatically by Compose

The app prints its configuration every few seconds so you can
see which values are being used.
"""

import os
import sys
import time

# ─────────────────────────────────────────────────
# Read ALL configuration from environment variables
# Each one has a sensible default so the app works even
# without any environment variables set
# ─────────────────────────────────────────────────
APP_NAME = os.environ.get("APP_NAME", "env-demo")
ENVIRONMENT = os.environ.get("ENVIRONMENT", "development")
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
POLL_INTERVAL = float(os.environ.get("POLL_INTERVAL", "5"))
API_KEY = os.environ.get("API_KEY", "(not set)")
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///default.db")
MAX_CONNECTIONS = int(os.environ.get("MAX_CONNECTIONS", "10"))


def print_config():
    """Print all configuration values so you can see what's being used."""
    print("=" * 50)
    print(f"  {APP_NAME} — Configuration")
    print("=" * 50)
    print(f"  APP_NAME        : {APP_NAME}")
    print(f"  ENVIRONMENT     : {ENVIRONMENT}")
    print(f"  LOG_LEVEL       : {LOG_LEVEL}")
    print(f"  POLL_INTERVAL   : {POLL_INTERVAL}s")
    print(f"  API_KEY         : {API_KEY}")
    print(f"  DATABASE_URL    : {DATABASE_URL}")
    print(f"  MAX_CONNECTIONS : {MAX_CONNECTIONS}")
    print("=" * 50)
    print()

    # Show which variables came from where
    print("  Variable origins:")
    print("    - APP_NAME, ENVIRONMENT  → set in docker-compose.yml 'environment'")
    print("    - API_KEY                → loaded from .env file by Compose")
    print("    - LOG_LEVEL              → ENV default in Dockerfile")
    print("    - Others                 → fallback defaults in app.py")
    print()


# Print config on startup
print_config()

# Main loop — print a heartbeat every POLL_INTERVAL seconds
print(f"Running... (printing every {POLL_INTERVAL}s)")
print("Try changing the .env file or docker-compose.yml and restart!")
print()

count = 0
while True:
    count += 1
    print(f"[{count:04d}] {APP_NAME} running in {ENVIRONMENT} mode")
    sys.stdout.flush()
    time.sleep(POLL_INTERVAL)
