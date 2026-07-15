"""
Lab A — Python Loop vs NumPy Vectorisation Benchmark

Students implement both approaches and use time.perf_counter() to
measure and compare normalising a 640×480×3 image over 1000 iterations.

Expected finding: NumPy is typically 100x or more faster. Students
should document the ratio and explain why in terms of:
  - NEON SIMD (hardware acceleration on ARM)
  - The GIL (Python loop runs interpreter overhead per element)
  - NumPy's C backend (compiled, vectorised, cache-friendly)
"""
import numpy as np
import time

# Create a realistic image (VGA resolution, 3 channels)
frame = np.random.randint(0, 256, (480, 640, 3), dtype=np.uint8)
N = 5  # number of iterations (pure Python loop is very slow on full VGA)

print(f"Image shape: {frame.shape}, dtype: {frame.dtype}")
print(f"Iterations: {N}")
print()

# --- Pure Python loop normalisation ---
print("Running Python loop normalisation...")
t0 = time.perf_counter()
for _ in range(N):
    # This is the slow way — iterating pixel by pixel in Python
    result = [[[px / 255.0 for px in row] for row in channel] for channel in frame]
t1 = time.perf_counter()
python_loop_ms = (t1 - t0) * 1000
print(f"Python loop: {python_loop_ms:.1f} ms total ({python_loop_ms / N:.3f} ms per frame)")

# --- NumPy vectorised normalisation ---
print("\nRunning NumPy vectorised normalisation...")
t0 = time.perf_counter()
for _ in range(N):
    result = frame.astype('float32') / 255.0
t1 = time.perf_counter()
numpy_vec_ms = (t1 - t0) * 1000
print(f"NumPy vectorised: {numpy_vec_ms:.1f} ms total ({numpy_vec_ms / N:.3f} ms per frame)")

# --- Comparison ---
speedup = python_loop_ms / numpy_vec_ms
print(f"\n=== Results ===")
print(f"Speedup: {speedup:.1f}x")
print(f"Python loop per frame:   {python_loop_ms / N:.3f} ms")
print(f"NumPy vectorised per frame: {numpy_vec_ms / N:.3f} ms")
print(f"\nNumPy is {speedup:.0f}x faster because:")
print(f"  - Uses compiled C code, not Python interpreter")
print(f"  - Leverages NEON SIMD for parallel pixel processing")
print(f"  - No per-element GIL overhead")
print(f"  - Cache-friendly contiguous memory access")
