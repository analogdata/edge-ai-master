#!/usr/bin/env python3
"""
FastAPI Server — Edge AI Results API
Analog Data — EdgeAI Engineering Bootcamp (Part 6)

This server:
  1. Subscribes to the MQTT topic where the inference engine publishes results
  2. Stores each result in a SQLite database
  3. Exposes REST API endpoints to query results

Endpoints:
  GET /              — health check
  GET /results/latest  — get the most recent inference result
  GET /results         — get all stored inference results
  GET /results/{frame} — get a specific result by frame number

Run locally:  uvicorn main:app --host 0.0.0.0 --port 8000
In Docker:    handled by the CMD in the Dockerfile
"""

import json
import logging
import os
import sqlite3
import threading
import time

import paho.mqtt.client as mqtt
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# ─────────────────────────────────────────────────
# Configuration from environment variables
# ─────────────────────────────────────────────────
MQTT_BROKER = os.environ.get("MQTT_BROKER", "mqtt")  # Docker service name
MQTT_PORT = int(os.environ.get("MQTT_PORT", "1883"))
MQTT_TOPIC = os.environ.get("MQTT_TOPIC", "sensors/inference")
DB_PATH = os.environ.get("DB_PATH", "/app/db/results.db")
API_KEY = os.environ.get("API_KEY", "")
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")

# ─────────────────────────────────────────────────
# Set up logging
# ─────────────────────────────────────────────────
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("edgeai-api")

# ─────────────────────────────────────────────────
# Pydantic model for inference results
# This defines the shape of the data returned by the API
# ─────────────────────────────────────────────────


class InferenceResult(BaseModel):
    """Data model for a single inference result."""

    frame: int
    label: str
    confidence: float
    timestamp: float


# ─────────────────────────────────────────────────
# SQLite database setup
# SQLite is built into Python — no external server needed
# ─────────────────────────────────────────────────


def init_db():
    """
    Create the SQLite database and results table if they don't exist.

    The database file is stored on a Docker named volume so data
    persists across container restarts.
    """
    # Ensure the directory exists
    db_dir = os.path.dirname(DB_PATH)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inference_results (
            frame       INTEGER PRIMARY KEY,
            label       TEXT NOT NULL,
            confidence  REAL NOT NULL,
            timestamp   REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()
    log.info(f"SQLite database initialized at {DB_PATH}")


def save_result(result: InferenceResult):
    """Save an inference result to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT OR REPLACE INTO inference_results (frame, label, confidence, timestamp)
        VALUES (?, ?, ?, ?)
    """,
        (result.frame, result.label, result.confidence, result.timestamp),
    )
    conn.commit()
    conn.close()


def get_latest_result() -> InferenceResult | None:
    """Retrieve the most recent inference result from the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT frame, label, confidence, timestamp "
        "FROM inference_results ORDER BY timestamp DESC LIMIT 1"
    )
    row = cursor.fetchone()
    conn.close()
    if row:
        return InferenceResult(frame=row[0], label=row[1], confidence=row[2], timestamp=row[3])
    return None


def get_all_results() -> list[InferenceResult]:
    """Retrieve all inference results from the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT frame, label, confidence, timestamp FROM inference_results ORDER BY timestamp DESC"
    )
    rows = cursor.fetchall()
    conn.close()
    return [
        InferenceResult(frame=row[0], label=row[1], confidence=row[2], timestamp=row[3])
        for row in rows
    ]


def get_result_by_frame(frame: int) -> InferenceResult | None:
    """Retrieve a specific inference result by frame number."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT frame, label, confidence, timestamp FROM inference_results WHERE frame = ?",
        (frame,),
    )
    row = cursor.fetchone()
    conn.close()
    if row:
        return InferenceResult(frame=row[0], label=row[1], confidence=row[2], timestamp=row[3])
    return None


# ─────────────────────────────────────────────────
# MQTT subscriber — listens for inference results
# Runs in a background thread so it doesn't block the API
# ─────────────────────────────────────────────────
def on_mqtt_message(client, userdata, msg):
    """Called when a new inference result arrives on the MQTT topic."""
    try:
        # Parse the JSON payload from the inference engine
        data = json.loads(msg.payload.decode())
        result = InferenceResult(**data)
        save_result(result)
        log.info(
            f"Stored result: frame={result.frame}, "
            f"label={result.label}, confidence={result.confidence:.2f}"
        )
    except Exception as e:
        log.error(f"Error processing MQTT message: {e}")


def start_mqtt_subscriber():
    """Start the MQTT subscriber in a background thread."""
    client = mqtt.Client(
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
        client_id="edgeai-api-subscriber",
    )
    client.on_message = on_mqtt_message

    # Retry connection in case the broker isn't ready yet
    while True:
        try:
            client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
            client.subscribe(MQTT_TOPIC)
            client.loop_start()
            log.info(f"Subscribed to MQTT topic: {MQTT_TOPIC}")
            break
        except Exception as e:
            log.warning(f"MQTT connection failed: {e}. Retrying in 5 seconds...")
            time.sleep(5)


# ─────────────────────────────────────────────────
# FastAPI application
# ─────────────────────────────────────────────────
app = FastAPI(
    title="Edge AI Results API",
    description="REST API for querying Edge AI inference results",
    version="1.0.0",
)


@app.on_event("startup")
def on_startup():
    """Initialize the database and start the MQTT subscriber on app startup."""
    init_db()
    # Start MQTT subscriber in a background thread
    threading.Thread(target=start_mqtt_subscriber, daemon=True).start()


@app.get("/")
def health_check():
    """Health check endpoint — confirms the API is running."""
    return {"status": "ok", "service": "edgeai-api", "version": "1.0.0"}


@app.get("/results/latest")
def get_latest():
    """Get the most recent inference result."""
    result = get_latest_result()
    if result is None:
        raise HTTPException(status_code=404, detail="No results found")
    return result


@app.get("/results")
def get_all():
    """Get all stored inference results, newest first."""
    results = get_all_results()
    if not results:
        raise HTTPException(status_code=404, detail="No results found")
    return results


@app.get("/results/{frame}")
def get_by_frame(frame: int):
    """Get a specific inference result by frame number."""
    result = get_result_by_frame(frame)
    if result is None:
        raise HTTPException(status_code=404, detail=f"No result found for frame {frame}")
    return result
