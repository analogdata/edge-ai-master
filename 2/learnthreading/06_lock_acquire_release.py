"""
06 — The Fix: threading.Lock() (acquire/release)

A Lock is like a key to a room. Only one person (thread) can hold the
key at a time. Others have to wait outside until the key is returned.

  lock.acquire()  — pick up the key (other threads must wait)
  lock.release()  — put the key back (next thread can proceed)

Now the counter is always 200000 — the lock ensures only one thread
increments at a time.
"""
import threading

counter = 0
lock = threading.Lock()   # create one lock


def add_one():
    global counter
    for _ in range(100000):
        lock.acquire()        # pick up the key — other threads must wait
        counter = counter + 1
        lock.release()        # put the key back — next thread can proceed


t1 = threading.Thread(target=add_one)
t2 = threading.Thread(target=add_one)

t1.start()
t2.start()

t1.join()
t2.join()

print(f"Counter value: {counter}")   # Now always: 200000
