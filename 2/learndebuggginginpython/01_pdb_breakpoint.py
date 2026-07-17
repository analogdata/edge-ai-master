"""
01 — pdb: Python Debugger Breakpoints
======================================
Demo: Using breakpoint() to pause execution and inspect live state.

Run:
    python 01_pdb_breakpoint.py

At the (Pdb) prompt try these commands:
    n          — next line (don't step into functions)
    s          — step into the function on this line
    c          — continue until next breakpoint
    p frame    — print the variable 'frame'
    pp frame   — pretty-print (useful for arrays / dicts)
    l          — list surrounding source code
    b 22       — set a breakpoint at line 22
    q          — quit debugger

Tip: In production, set PYTHONBREAKPOINT=0 to disable all breakpoints.
     export PYTHONBREAKPOINT=0
"""

import numpy as np


def preprocess(frame):
    """Simulate image preprocessing for an Edge AI inference pipeline."""
    frame = frame.astype("float32")
    breakpoint()  # execution pauses here — inspect 'frame'
    frame = frame / 255.0  # normalise to [0, 1]
    frame = np.resize(frame, (224, 224, 3))  # resize for model input
    return frame


def run_inference(frame):
    """Simulate a model inference call."""
    result = {"class": "person", "confidence": 0.92, "latency_ms": 14.3}
    return result


if __name__ == "__main__":
    # Simulate a raw camera frame: 480x640x3 uint8
    raw_frame = np.random.randint(0, 256, (480, 640, 3), dtype=np.uint8)

    print("Raw frame:", raw_frame.shape, raw_frame.dtype)

    processed = preprocess(raw_frame)
    print("Processed frame:", processed.shape, processed.dtype)

    output = run_inference(processed)
    print("Inference result:", output)
