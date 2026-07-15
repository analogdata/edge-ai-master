"""
13 — Generator Functions for Streaming Frames

A generator uses `yield` instead of `return`. Instead of computing all
values up front and storing them in a list, it produces one value at a
time, on demand. For a camera pipeline that could run forever, this is
the only sane approach — you cannot load thousands of frames into a
list before starting inference.

This example simulates a camera with a generator so it runs without
requiring an actual camera or OpenCV.
"""
import time


def frame_stream(num_frames=5):
    """Simulates yielding frames one at a time from a camera.

    In real code this would be:
        def frame_stream(cap):
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                yield frame
    """
    for i in range(num_frames):
        # Simulate capturing a frame (in real code: cap.read())
        frame = f"frame_{i}"
        print(f"  [Generator] Captured {frame}")
        yield frame


def run_inference(frame):
    """Simulates running AI inference on a frame."""
    print(f"  [Inference] Processing {frame}...")
    time.sleep(0.1)
    return f"result_for_{frame}"


# Using the generator — each frame is processed one at a time
# No list of all frames exists in memory
for frame in frame_stream(num_frames=5):
    result = run_inference(frame)
    print(f"  [Display] {result}")
    print()
