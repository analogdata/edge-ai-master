"""
02 — Your First Thread

A thread is like an independent worker that runs your function separately
in the background. When you start a thread, Python doesn't wait for it to
finish — it moves on immediately.

Total time: ~3 seconds (instead of 9) because all three downloads happen
at the same time.

Key methods:
  - threading.Thread(target=fn, args=(...))  — creates a thread (doesn't run it yet)
  - .start()  — starts running the function in the background
  - .join()   — waits until the thread finishes
"""
import threading
import time


def download_file(name):
    print(f"Downloading {name}...")
    time.sleep(3)
    print(f"{name} downloaded!")


# Create a thread for each file
t1 = threading.Thread(target=download_file, args=("file_1.txt",))
t2 = threading.Thread(target=download_file, args=("file_2.txt",))
t3 = threading.Thread(target=download_file, args=("file_3.txt",))

# Start all three threads — they run simultaneously
t1.start()
t2.start()
t3.start()

# Wait for all threads to finish
t1.join()
t2.join()
t3.join()

print("All done!")
