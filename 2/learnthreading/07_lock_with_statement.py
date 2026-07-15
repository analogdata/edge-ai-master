"""
07 — Better Way: Using `with lock:` (Recommended Always)

The `with` statement automatically acquires and releases the lock —
even if an error happens inside the block. This is cleaner and safer
than manually calling acquire()/release().

Simple rule: Any time two or more threads read AND write the same
variable, protect it with a Lock.
"""
import threading

counter = 0
lock = threading.Lock()


def add_one():
    global counter
    for _ in range(100000):
        with lock:            # acquires lock here
            counter += 1     # only one thread runs this at a time
                             # lock released automatically when block ends


t1 = threading.Thread(target=add_one)
t2 = threading.Thread(target=add_one)

t1.start()
t2.start()

t1.join()
t2.join()

print(f"Counter value: {counter}")   # Always: 200000
