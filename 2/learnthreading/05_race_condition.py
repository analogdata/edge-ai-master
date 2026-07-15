"""
05 — The Shared Variable Problem: Race Condition

When two threads share the same variable and both read AND write it,
they can accidentally overwrite each other's work. This is called a
race condition.

The counter should be 200000 (100000 + 100000), but you'll get a
different (smaller) number every time — because both threads read
the same value, add 1, and write back, losing one increment.

This is like two people editing the same Google Doc word at the same
time — they overwrite each other.
"""
import threading

counter = 0   # shared variable


def add_one():
    global counter
    for _ in range(100000):
        counter = counter + 1   # both threads do this at the same time


t1 = threading.Thread(target=add_one)
t2 = threading.Thread(target=add_one)

t1.start()
t2.start()

t1.join()
t2.join()

print(f"Counter value: {counter}")
# Expected: 200000
# Actual: something like 147823 — different every time!
