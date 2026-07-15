"""
09 — queue.Queue: Safe Way to Pass Data Between Threads

A Queue is like a conveyor belt between threads. One thread puts items
on it, another thread picks items off it. The Queue handles all the
safety and waiting automatically — you don't need a Lock.

  q.put(item)    — add to the queue
  q.get()        — take from queue (waits if empty)
  q.task_done()  — tell the queue this item is processed
"""
import threading
import queue
import time


def producer(q):
    """Puts items into the queue."""
    for i in range(5):
        item = f"item_{i}"
        q.put(item)            # add to the queue
        print(f"[Producer] Put {item}")
        time.sleep(0.5)


def consumer(q):
    """Takes items from the queue."""
    for i in range(5):
        item = q.get()         # take from queue — waits if queue is empty
        print(f"[Consumer] Got {item}")
        q.task_done()          # tell the queue this item is processed


# Create a queue
q = queue.Queue()

t1 = threading.Thread(target=producer, args=(q,))
t2 = threading.Thread(target=consumer, args=(q,))

t1.start()
t2.start()

t1.join()
t2.join()
