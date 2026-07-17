"""
03 — cProfile + pstats: Function-Level Profiling
=================================================
Demo: Profile a simulated inference pipeline and find the slowest functions.

Run from command line (no code changes needed):
    python -m cProfile -o profile_output.prof 03_cprofile_pstats.py

Then inspect the profile:
    python -m pstats profile_output.prof
    > sort cumulative
    > stats 20

Or run this script directly — it profiles itself and prints the top 20:
    python 03_cprofile_pstats.py

Key columns in pstats output:
  ncalls   — number of times the function was called
  tottime  — time inside this function only (excludes sub-calls)
  cumtime  — total time including all functions this one called
  percall  — time per call (tottime or cumtime / ncalls)

Teaching point: Start with 'cumulative' sort — it tells you which function
(including everything it triggers) dominates runtime.
"""

import cProfile
import pstats
import time
import numpy as np


def generate_frames(n=100):
    """Simulate capturing n frames from a camera."""
    frames = []
    for _ in range(n):
        frame = np.random.randint(0, 256, (480, 640, 3), dtype=np.uint8)
        frames.append(frame)
    return frames


def preprocess(frame):
    """Simulate image preprocessing: cast, normalise, resize."""
    frame = frame.astype("float32")
    frame = frame / 255.0
    frame = np.resize(frame, (224, 224, 3))
    return frame


def run_inference(frame):
    """Simulate a model inference call (the 'expensive' part)."""
    time.sleep(0.01)  # simulate model latency
    return {"class": "person", "confidence": 0.92}


def inference_pipeline(n_frames=100):
    """Full pipeline: generate → preprocess → infer."""
    frames = generate_frames(n_frames)
    results = []
    for frame in frames:
        processed = preprocess(frame)
        result = run_inference(processed)
        results.append(result)
    return results


if __name__ == "__main__":
    profiler = cProfile.Profile()
    profiler.enable()

    results = inference_pipeline(n_frames=100)

    profiler.disable()

    stats = pstats.Stats(profiler)
    stats.sort_stats("cumulative")  # sort by cumulative time
    stats.print_stats(20)           # show top 20 functions

    print(f"\nProcessed {len(results)} frames")
    print("\n--- Try also from the command line ---")
    print("python -m cProfile -o profile_output.prof 03_cprofile_pstats.py")
    print("python -m pstats profile_output.prof")
    print("> sort cumulative")
    print("> stats 20")
