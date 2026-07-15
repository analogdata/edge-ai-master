"""
Lab B — Thread-Safe Frame Ring Buffer

Students implement a ring buffer using threading.Thread + queue.Queue
where the producer is a camera capture loop and the consumer prints
the frame shape and timestamp. They must demonstrate it runs without
deadlocking and handles queue-full conditions gracefully by dropping
frames.

This implementation:
  - Producer simulates camera capture at ~30 FPS (33ms intervals)
  - Consumer simulates slow processing (~100ms per frame)
  - Bounded queue (maxsize=3) forces frame drops when consumer falls behind
  - daemon=True on both threads prevents zombie threads
  - Graceful shutdown after N frames
"""
import threading
import queue
import time
import numpy as np

QUEUE_MAXSIZE = 3  # small buffer to force frame drops
TOTAL_FRAMES = 15


def producer(frame_queue, num_frames):
    """Simulates camera capture at ~30 FPS.

    Uses put_nowait to avoid blocking — if the queue is full, the
    frame is dropped (stale frames have no value in real-time systems).
    """
    for i in range(num_frames):
        # Simulate a camera frame (480x640x3 uint8)
        frame = np.random.randint(0, 256, (480, 640, 3), dtype=np.uint8)
        timestamp = time.perf_counter()

        try:
            frame_queue.put_nowait((i, frame, timestamp))
            print(f"  [Producer] Frame {i:2d} captured  (queue: {frame_queue.qsize()})")
        except queue.Full:
            print(f"  [Producer] Frame {i:2d} DROPPED   (queue full!)")

        time.sleep(0.033)  # ~30 FPS

    # Signal the consumer that production is done
    frame_queue.put(None)


def consumer(frame_queue):
    """Simulates slow inference (~100ms per frame).

    queue.get() blocks until a frame is available — zero CPU while waiting.
    Prints frame shape and timestamp for each processed frame.
    """
    while True:
        item = frame_queue.get()
        if item is None:  # sentinel — producer is done
            frame_queue.task_done()
            break

        frame_id, frame, timestamp = item
        queue_wait = time.perf_counter() - timestamp

        print(f"  [Consumer] Frame {frame_id:2d} | shape: {frame.shape} "
              f"| waited {queue_wait*1000:.1f}ms in queue")

        time.sleep(0.1)  # simulate slow inference (~100ms)
        frame_queue.task_done()


# Create a bounded queue
frame_queue = queue.Queue(maxsize=QUEUE_MAXSIZE)

# Create daemon threads
t_producer = threading.Thread(target=producer, args=(frame_queue, TOTAL_FRAMES), daemon=True)
t_consumer = threading.Thread(target=consumer, args=(frame_queue,), daemon=True)

print(f"=== Thread-Safe Frame Ring Buffer ===")
print(f"Queue maxsize: {QUEUE_MAXSIZE}")
print(f"Total frames to capture: {TOTAL_FRAMES}")
print(f"Producer: ~30 FPS (33ms intervals)")
print(f"Consumer: ~10 FPS (100ms per frame)")
print(f"Expected: some frames will be dropped due to slow consumer\n")

t_producer.start()
t_consumer.start()

t_producer.join()
t_consumer.join()

print(f"\n=== Done ===")
print("No deadlocks occurred. Frame drops are expected when consumer is slower than producer.")
