"""
15 — Producer/Consumer with threading.Thread + queue.Queue

The simple generator pipeline is still sequential — capture, then
preprocess, then infer, one frame at a time. On a system where capture
takes ~10ms and inference takes ~80ms, the camera sits idle for 80ms
per frame.

The solution: decouple capture from inference using threads and a
shared queue.

  [Producer Thread] → queue.Queue → [Consumer Thread]
   (camera capture)                   (model inference)

Key design decisions:
  - queue.Queue(maxsize=5): caps memory; prevents producer from running
    hundreds of frames ahead of the slow consumer
  - put_nowait + except queue.Full: drop frames rather than block capture
    (stale frames have no value in a real-time system)
  - daemon=True: threads auto-terminate when main program exits
  - queue.get() blocks: consumer naturally sleeps when queue is empty,
    consuming zero CPU while it waits
"""
import threading
import queue
import time

QUEUE_MAXSIZE = 5  # don't let the buffer grow unbounded


def producer(frame_queue, num_frames=10):
    """Captures frames and puts them in the queue.

    In real code: cap.read() in a while True loop.
    Uses put_nowait to avoid blocking — drops frames if queue is full.
    Sends a None sentinel when done so the consumer knows to stop.
    """
    for i in range(num_frames):
        frame = f"frame_{i}"
        try:
            frame_queue.put_nowait(frame)   # non-blocking; drop if queue is full
            print(f"  [Producer] Put {frame}  (queue size: {frame_queue.qsize()})")
        except queue.Full:
            print(f"  [Producer] DROPPED {frame} — queue full!")
        time.sleep(0.05)  # simulate capture time (~10ms)

    # Signal the consumer that production is finished
    frame_queue.put(None)


def consumer(frame_queue):
    """Reads frames from the queue and runs inference.

    queue.get() blocks until a frame is available — zero CPU while waiting.
    Stops when it receives None (the sentinel from the producer).
    In real code: model.infer(frame)
    """
    while True:
        frame = frame_queue.get()           # blocks until a frame is available
        if frame is None:                   # sentinel — producer is done
            frame_queue.task_done()
            break
        print(f"  [Consumer] Got {frame}  (queue size: {frame_queue.qsize()})")
        time.sleep(0.2)                     # simulate inference time (~80ms)
        frame_queue.task_done()


# Create a bounded queue
frame_queue = queue.Queue(maxsize=QUEUE_MAXSIZE)

# Create daemon threads — they auto-terminate when main program exits
t_producer = threading.Thread(target=producer, args=(frame_queue, 10), daemon=True)
t_consumer = threading.Thread(target=consumer, args=(frame_queue,), daemon=True)

t_producer.start()
t_consumer.start()

t_producer.join()
t_consumer.join()

print("\nAll frames processed!")
