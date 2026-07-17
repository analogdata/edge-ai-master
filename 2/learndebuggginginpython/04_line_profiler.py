import numpy as np

# 04 - line_profiler: Line-by-Line Timing
# ========================================
# Demo: Find the slowest line INSIDE a function using @profile decorator.
#
# Installation:
#     pip install line_profiler
#
# Run with kernprof:
#     kernprof -l -v 04_line_profiler.py
#
# Sample output (your numbers will vary):
#
#     Timer unit: 1e-06 s
#
#     Total time: 0.040349 s
#     File: 04_line_profiler.py
#     Function: preprocess at line 33
#
#     Line #      Hits         Time  Per Hit   % Time  Line Contents
#     ==============================================================
#         33                                           @profile
#         34                                           def preprocess(frame):
#         35                                               """Simulate image preprocessing..."""
#         36       100      26167.0    261.7     64.9      frame = frame.astype("float32")
#         37       100       7716.0     77.2     19.1      frame = frame / 255.0
#         38       100       5893.0     58.9     14.6      frame = np.resize(frame, (224, 224, 3))
#         39       100        558.0      5.6      1.4      frame = np.expand_dims(frame, axis=0)
#         40       100         15.0      0.1      0.0      return frame
#
# How to read each column:
#   Line #        - the line number in the source file (matches the Line Contents)
#   Hits          - how many times this line was executed during the run
#                   (100 here = 100 frames x 1 call per frame)
#   Time          - total microseconds spent on this line across ALL hits
#                   (26167 us = 0.026 seconds total on line 36)
#   Per Hit       - average time per single execution (Time / Hits)
#                   (26167 / 100 = 261.7 us per call)
#   % Time        - this line's share of the TOTAL function time
#                   (26167 / 40349 = 64.9% - line 36 eats almost 2/3 of runtime)
#   Line Contents - the actual source code for that line
#
# Key observations from this output:
#   1. Line 36 (astype) is the bottleneck at 64.9% - it allocates a new float32
#      array, copying 480x640x3 = 921,600 values from uint8 to float32.
#   2. Line 37 (division by 255) is 19.1% - allocates ANOTHER new array.
#   3. Line 38 (resize) is only 14.6% - surprisingly cheap because it's vectorised
#      in C, unlike the Python-level allocation overhead of astype.
#   4. Line 39 (expand_dims) is 1.4% - negligible; just adds a batch dimension.
#
# What you should look for:
#   - Sort by % Time - the highest number is your bottleneck line
#   - If one line is >50%, that's where to focus optimisation effort
#   - Compare Per Hit across lines to understand per-operation cost
#   - Hits tells you if a line runs in a hot loop (high count = optimise first)
#   - Don't trust intuition - measure. Developers often guess the wrong line.
#
# Common optimisation strategies after finding the bottleneck:
#   - Replace Python loops with NumPy vectorised operations
#   - Use in-place operations (out= parameter) to avoid array copies
#   - Combine operations: img.astype('float32') / 255.0  (one copy, not two)
#   - Pre-allocate buffers outside loops instead of inside
#   - Use cv2.resize() instead of np.resize() for image resizing (faster)
#
# Teaching point: Profile first, find the real bottleneck, optimise, re-profile.
# Workflow: cProfile -> find slow function -> line_profiler -> find slow line -> optimise -> re-profile
#
# The @profile decorator is injected by kernprof at runtime - no import needed.
# Just decorate the function you want to profile line-by-line.


@profile
def preprocess(frame):
    """Simulate image preprocessing — which line is the bottleneck?"""
    frame = frame.astype("float32")          # line A: cast to float
    frame = frame / 255.0                    # line B: normalise
    frame = np.resize(frame, (224, 224, 3))  # line C: resize for model
    frame = np.expand_dims(frame, axis=0)    # line D: add batch dimension
    return frame


def run_inference(frame):
    """Simulate model inference."""
    return {"class": "person", "confidence": 0.92}


if __name__ == "__main__":
    # Generate 100 frames and preprocess each
    for _ in range(100):
        raw = np.random.randint(0, 256, (480, 640, 3), dtype=np.uint8)
        processed = preprocess(raw)
        result = run_inference(processed)

    print("Done. Run with: kernprof -l -v 04_line_profiler.py")
