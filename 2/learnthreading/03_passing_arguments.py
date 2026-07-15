"""
03 — Passing Arguments to a Thread

You can pass any number of positional arguments using args (must be a tuple).
For keyword arguments, use kwargs (a dictionary).

Remember: args=("hello",) — that trailing comma is required for a single-item tuple!
Without the comma, Python treats ("hello") as just a string in parentheses.
"""
import threading
import time


def greet(name, times):
    for i in range(times):
        print(f"Hello, {name}! (message {i+1})")
        time.sleep(1)


# Using args (positional arguments)
t = threading.Thread(target=greet, args=("Rahul", 3))
t.start()
t.join()

print("---")

# Using kwargs (keyword arguments)
t = threading.Thread(target=greet, kwargs={"name": "Rahul", "times": 3})
t.start()
t.join()
