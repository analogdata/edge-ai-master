"""
05 — memory_profiler: Per-Line Memory Tracking
================================================
Demo: Track how much RAM each line allocates inside a function.

Installation:
    pip install memory_profiler

Run:
    python -m memory_profiler 05_memory_profiler.py

Sample output:
    Line #  Mem usage   Increment  Line Contents
    5       52.3 MiB    52.3 MiB   img = cv2.imread(image_path)
    6       53.7 MiB    1.4 MiB    img_float = img.astype('float32')
    7       55.2 MiB    1.5 MiB    img_norm = img_float / 255.0
    8       55.2 MiB    0.0 MiB    batch = np.expand_dims(img_norm, axis=0)
    9       127.8 MiB   72.6 MiB   result = model.infer(batch)

What to look for:
  Lines 6 and 7 each allocate a full copy of the image.
  Fix: combine into one operation →  img_norm = img.astype('float32') / 255.0

Teaching point: On a Pi with 1-4GB RAM, a memory leak of even 1MB/frame
will OOM-kill the process in minutes. If the Increment column keeps growing
across iterations, that line is leaking.
"""

import numpy as np
from memory_profiler import profile


@profile
def load_and_infer():
    """Simulate loading an image and running inference — watch memory grow."""
    # Simulate a 640x480x3 uint8 image (like a camera frame)
    img = np.random.randint(0, 256, (480, 640, 3), dtype=np.uint8)  # line A

    # Each of these allocates a NEW array — watch the Increment column
    img_float = img.astype("float32")       # line B — allocates a full copy
    img_norm = img_float / 255.0            # line C — allocates ANOTHER copy
    batch = np.expand_dims(img_norm, axis=0)  # line D — small overhead

    # Simulate model inference (in real life this loads weights etc.)
    result = np.random.rand(1, 1000)        # line E — model output
    return result


@profile
def load_and_infer_optimised():
    """Same logic but with in-place / combined operations — less memory."""
    img = np.random.randint(0, 256, (480, 640, 3), dtype=np.uint8)

    # One intermediate instead of two
    img_norm = img.astype("float32") / 255.0

    batch = np.expand_dims(img_norm, axis=0)
    result = np.random.rand(1, 1000)
    return result


# WHY MEMORY WAS REDUCED - Explanation
# ======================================
#
# UNOPTIMISED (two separate operations):
#   Line 40:  img_float = img.astype("float32")       +3.5 MiB
#   Line 41:  img_norm = img_float / 255.0            +3.5 MiB
#   ---
#   Total peak allocation from these two lines: 7.0 MiB
#
#   Step 1: astype("float32") creates a NEW float32 array (3.5 MiB).
#           uint8 uses 1 byte per pixel, float32 uses 4 bytes per pixel.
#           480 x 640 x 3 x 4 bytes = 3,686,400 bytes = ~3.5 MiB
#           At this point BOTH img (uint8) AND img_float (float32) exist.
#
#   Step 2: / 255.0 creates ANOTHER NEW array (3.5 MiB).
#           The division does not modify img_float in place.
#           It allocates a fresh array for the result.
#           At this point THREE arrays exist simultaneously:
#             img       (uint8)      ~0.9 MiB
#             img_float (float32)    ~3.5 MiB  <- intermediate, no longer needed
#             img_norm  (float32)    ~3.5 MiB  <- the one we actually use
#
#   Peak memory during these two lines: ~7.0 MiB for the two float32 copies.
#   The intermediate img_float is garbage-collected only AFTER line 41 finishes.
#
# OPTIMISED (one combined operation):
#   Line 55:  img_norm = img.astype("float32") / 255.0   +0.0 MiB
#
#   astype("float32") creates a temporary float32 array, but the / 255.0
#   division is chained immediately. Python evaluates this as a single
#   expression, so the temporary from astype() is never bound to a variable.
#   The garbage collector can free it as soon as the division produces
#   img_norm. Only ONE float32 array survives: img_norm.
#
#   Peak memory: ~3.5 MiB for the single float32 result.
#   Savings: ~3.5 MiB per frame (50% reduction in intermediate allocations).
#
# WHY THIS MATTERS ON EDGE HARDWARE:
#   On a Raspberry Pi with 1-4 GB RAM, saving 3.5 MiB per frame is huge.
#   If you process 30 frames/second, that's 105 MiB/s of avoided allocation
#   churn. Less allocation = less GC pressure = lower latency = fewer OOM kills.
#
#   In a loop of 1000 frames, the unoptimised version temporarily holds
#   2 x 3.5 = 7 MiB of float32 arrays on every iteration. The optimised
#   version never holds more than 1 x 3.5 = 3.5 MiB at any point.
#
# KEY TAKEAWAY:
#   Chain operations into a single expression so temporaries are short-lived.
#   Each variable you assign creates a reference that keeps the array alive.
#   Fewer variables = fewer simultaneous arrays = lower peak memory.


if __name__ == "__main__":
    print("=== Unoptimised version (two copies) ===")
    load_and_infer()

    print("\n=== Optimised version (one copy) ===")
    load_and_infer_optimised()

    print("\nRun with: python -m memory_profiler 05_memory_profiler.py")
