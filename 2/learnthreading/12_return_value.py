"""
12 — Getting a Return Value from a Thread

Threads don't return values directly. The easiest beginner approach
is to use a list or dictionary to collect results.

Here we use a shared dictionary — each thread writes its result
under its own key. Since each thread writes to a DIFFERENT key,
there's no race condition and no lock needed.
"""
import threading

results = {}   # shared dictionary to store results


def square(number):
    results[number] = number * number


threads = []
for n in [2, 4, 6, 8, 10]:
    t = threading.Thread(target=square, args=(n,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print(results)
# {2: 4, 4: 16, 6: 36, 8: 64, 10: 100}
