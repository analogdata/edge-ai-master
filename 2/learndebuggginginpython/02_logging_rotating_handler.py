"""
02 — Structured Logging with RotatingFileHandler
==================================================
Demo: Console + rotating file logging for an Edge AI inference loop.

Why not print()?
  - print() goes to stdout, lost when terminal closes
  - No timestamps, no severity levels, no per-module control
  - On a headless Pi running systemd, print() is invisible

RotatingFileHandler caps log size:
  maxBytes=5MB, backupCount=3  →  max 20MB total (5MB x 4 files)
  This prevents logs from filling the SD card on a Pi.

Run:
    python 02_logging_rotating_handler.py

Check the log file:
    cat inference.log
"""

import logging
from logging.handlers import RotatingFileHandler
import time
import random

# ---------------------------------------------------------------------------
# 1. Create a logger
# ---------------------------------------------------------------------------
logger = logging.getLogger("edge_ai_app")
logger.setLevel(logging.DEBUG)  # capture everything; handlers filter further

# ---------------------------------------------------------------------------
# 2. Console handler — for development (INFO and above)
# ---------------------------------------------------------------------------
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# ---------------------------------------------------------------------------
# 3. Rotating file handler — for production (DEBUG and above)
#    maxBytes=5MB, backupCount=3  →  4 files x 5MB = 20MB max footprint
# ---------------------------------------------------------------------------
file_handler = RotatingFileHandler(
    filename="inference.log",
    maxBytes=5 * 1024 * 1024,  # 5 MB per file
    backupCount=3,             # keep 3 rotated files
)
file_handler.setLevel(logging.DEBUG)

# ---------------------------------------------------------------------------
# 4. Formatter — timestamp | level | logger name | message
# ---------------------------------------------------------------------------
formatter = logging.Formatter(
    fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# ---------------------------------------------------------------------------
# 5. Attach handlers
# ---------------------------------------------------------------------------
logger.addHandler(console_handler)
logger.addHandler(file_handler)


def simulate_inference_loop(n_frames=20):
    """Simulate processing frames with logging at every severity level."""
    logger.info("Inference service started")

    for i in range(n_frames):
        # Simulate variable inference latency
        latency_ms = random.uniform(8.0, 25.0)
        confidence = random.uniform(0.5, 0.99)

        logger.debug("Frame %d captured: latency_ms=%.1f", i, latency_ms)

        if confidence < 0.6:
            logger.warning("Low confidence on frame %d: %.3f", i, confidence)

        if latency_ms > 22.0:
            logger.error("High latency on frame %d: %.1fms — possible frame drop", i, latency_ms)

        # Simulate a critical failure on the last frame
        if i == n_frames - 1 and random.random() < 0.3:
            logger.critical("Memory threshold exceeded — shutting down gracefully")
            return

        logger.info("Frame %d done: class=person confidence=%.3f latency_ms=%.1f",
                     i, confidence, latency_ms)
        time.sleep(0.05)

    logger.info("Inference loop complete — processed %d frames", n_frames)


if __name__ == "__main__":
    simulate_inference_loop(n_frames=20)
    print("\nLog written to 'inference.log'")
    print("Run multiple times to see rotation in action.")
