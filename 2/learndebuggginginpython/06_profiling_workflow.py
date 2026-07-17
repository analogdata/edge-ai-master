"""
06 — Complete Profiling Workflow
=================================
Putting it all together: cProfile → line_profiler → optimise → re-profile

This script demonstrates the full workflow taught in the lecture:
  1. Run cProfile to find the slowest FUNCTION
  2. Use line_profiler on that function to find the slowest LINE
  3. Optimise the bottleneck line
  4. Re-profile to confirm improvement

Run:
    python 06_profiling_workflow.py

Then try line_profiler on the bottleneck:
    kernprof -l -v 06_profiling_workflow.py
"""

import cProfile
import pstats
import time
import numpy as np


# ---------------------------------------------------------------------------
# UNOPTIMISED version — has an obvious bottleneck in preprocess()
# ---------------------------------------------------------------------------

def preprocess_slow(frame):
    """Simulate preprocessing with an intentional bottleneck."""
    frame = frame.astype("float32")
    frame = frame / 255.0
    # Intentionally slow: resize pixel-by-pixel instead of using np.resize
    h, w = 224, 224
    resized = np.zeros((h, w, 3), dtype=np.float32)
    for i in range(h):
        for j in range(w):
            resized[i, j] = frame[i * 2, j * 2]  # naive downsampling
    batch = np.expand_dims(resized, axis=0)
    return batch


def preprocess_fast(frame):
    """Optimised version — uses vectorised np.resize instead of loops."""
    frame = frame.astype("float32")
    frame = frame / 255.0
    resized = np.resize(frame, (224, 224, 3))  # vectorised — much faster
    batch = np.expand_dims(resized, axis=0)
    return batch


def run_inference(batch):
    """Simulate model inference."""
    time.sleep(0.005)
    return {"class": "person", "confidence": 0.92}


def pipeline(preprocess_fn, n_frames=50):
    """Run the full pipeline with a given preprocess function."""
    results = []
    for _ in range(n_frames):
        raw = np.random.randint(0, 256, (448, 448, 3), dtype=np.uint8)
        processed = preprocess_fn(raw)
        result = run_inference(processed)
        results.append(result)
    return results


def profile_pipeline(label, preprocess_fn, n_frames=50):
    """Profile a pipeline run and print the top 10 functions."""
    print(f"\n{'='*60}")
    print(f"  Profiling: {label}  ({n_frames} frames)")
    print(f"{'='*60}")

    profiler = cProfile.Profile()
    profiler.enable()
    results = pipeline(preprocess_fn, n_frames)
    profiler.disable()

    stats = pstats.Stats(profiler)
    stats.sort_stats("cumulative")
    stats.print_stats(10)
    print(f"  Processed {len(results)} frames\n")


if __name__ == "__main__":
    # Step 1: Profile the SLOW version
    profile_pipeline("SLOW (nested loops in preprocess)", preprocess_slow, n_frames=30)

    # Step 2: Profile the FAST version
    profile_pipeline("FAST (vectorised np.resize)", preprocess_fast, n_frames=30)

    print("="*60)
    print("  WORKFLOW RECAP")
    print("="*60)
    print("  1. cProfile  → found preprocess_slow as the bottleneck")
    print("  2. line_profiler → would show the nested for-loop as 96%+ of time")
    print("  3. Optimise  → replaced loops with np.resize (vectorised)")
    print("  4. Re-profile → confirm the speedup (compare cumtime)")
    print()
    print("  Try line_profiler on this file:")
    print("    kernprof -l -v 06_profiling_workflow.py")
