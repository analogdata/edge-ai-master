"""
10 — Limiting Queue Size

You can limit how many items the queue holds at once. If the queue
is full, the producer's q.put() will automatically wait until the
consumer removes an item.

This is useful for backpressure — preventing a fast producer from
flooding memory when the consumer is slow.

  queue.Queue(maxsize=3)  — holds at most 3 items at a time
"""
import threading
import queue
import time


def producer(q):
    """Puts items into the queue. Will wait if queue is full."""
    for i in range(10):
        item = f"item_{i}"
        q.put(item)            # waits here if queue is full
        print(f"[Producer] Put {item}")
        time.sleep(0.2)


def consumer(q):
    """Takes items from the queue. Slower than producer."""
    for i in range(10):
        item = q.get()
        print(f"[Consumer] Got {item}")
        q.task_done()
        time.sleep(1)          # consumer is slow — producer will have to wait


# Create a queue with a maximum size of 3
q = queue.Queue(maxsize=3)

t1 = threading.Thread(target=producer, args=(q,))
t2 = threading.Thread(target=consumer, args=(q,))

t1.start()
t2.start()

t1.join()
t2.join()

print("All items processed!")
