"""
17 — time.perf_counter(): Microsecond Profiling

Before optimising anything, measure it. time.perf_counter() is the
highest-resolution timer available in Python — suitable for microsecond-
level measurements.

Why not time.time()?
  - time.time() returns wall-clock time with second-resolution on some
    systems
  - time.perf_counter() uses the highest available hardware counter and
    is monotonic (it never goes backward due to NTP adjustments or
    system clock changes)

This example builds a simple frame-rate profiler that measures
inference time and computes effective FPS.
"""
import time


def simulate_inference(frame_id):
    """Simulates running AI inference on a frame."""
    time.sleep(0.080)  # simulate ~80ms inference time
    return f"result_{frame_id}"


def simulate_frame_stream(num_frames=10):
    """Simulates a stream of frames from a camera."""
    for i in range(num_frames):
        time.sleep(0.010)  # simulate ~10ms capture time
        yield i


# --- Basic profiling: measure a single operation ---
print("=== Single Operation Profiling ===")
start = time.perf_counter()
result = simulate_inference(0)
end = time.perf_counter()
elapsed_ms = (end - start) * 1000
print(f"Inference time: {elapsed_ms:.3f} ms")
print()

# --- Building a frame-rate profiler ---
print("=== Frame-Rate Profiler ===")
frame_times = []

for frame in simulate_frame_stream(num_frames=10):
    t0 = time.perf_counter()
    result = simulate_inference(frame)
    t1 = time.perf_counter()
    frame_time = t1 - t0
    frame_times.append(frame_time)
    print(f"  Frame {frame}: {(frame_time * 1000):.2f} ms")

avg_ms = sum(frame_times) / len(frame_times) * 1000
fps = 1.0 / (sum(frame_times) / len(frame_times))
print(f"\nAverage inference: {avg_ms:.2f} ms | Effective FPS: {fps:.1f}")
