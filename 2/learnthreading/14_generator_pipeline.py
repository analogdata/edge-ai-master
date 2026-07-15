"""
14 — Composing Generators into a Pipeline

Generators can be wrapped inside each other to build a clean
preprocessing pipeline. Each stage processes exactly one frame at a
time and hands it forward — no intermediate list exists in memory.

This pattern scales from a Pi Zero 2W to a Pi 5 without changing
the pipeline architecture.

Pipeline:
  frame_stream  →  resize_stream  →  normalize_stream  →  inference

In real code, each stage uses cv2 / NumPy. Here we simulate with
plain Python so it runs without dependencies.
"""
import time


def frame_stream(num_frames=5):
    """Stage 1: Capture frames one at a time."""
    for i in range(num_frames):
        frame = {"id": i, "resolution": (640, 480), "data": f"raw_{i}"}
        print(f"  [Capture] {frame['id']}: {frame['resolution']}")
        yield frame


def resize_stream(frames, size=(320, 240)):
    """Stage 2: Resize each frame."""
    for frame in frames:
        frame = frame.copy()
        frame["resolution"] = size
        print(f"  [Resize]   {frame['id']}: {frame['resolution']}")
        yield frame


def normalize_stream(frames):
    """Stage 3: Normalize each frame to 0.0–1.0 range."""
    for frame in frames:
        frame = frame.copy()
        frame["normalized"] = True
        print(f"  [Normalize] {frame['id']}: normalized=True")
        yield frame


def run_inference(frame):
    """Stage 4: Run AI inference on the preprocessed frame."""
    print(f"  [Inference] {frame['id']}: done")
    return f"result_for_{frame['id']}"


# Compose the pipeline — each generator wraps the previous one
# No intermediate lists — each frame flows through one stage at a time
pipeline = normalize_stream(resize_stream(frame_stream(num_frames=5)))

for preprocessed_frame in pipeline:
    result = run_inference(preprocessed_frame)
    print(f"  => {result}\n")
