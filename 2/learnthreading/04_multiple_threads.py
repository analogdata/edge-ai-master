"""
04 — Running Multiple Threads Together (Cleaner Way)

When you have many threads, use a list to manage them instead of creating
individual variables (t1, t2, t3, ...). This scales to any number of threads.

The output order may vary — threads run concurrently and the OS decides
which one gets to print at any given moment.
"""
import threading
import time


def task(task_number):
    print(f"Task {task_number} started")
    time.sleep(2)
    print(f"Task {task_number} finished")


# Create 5 threads using a list
threads = []
for i in range(1, 6):
    t = threading.Thread(target=task, args=(i,))
    threads.append(t)

# Start all threads
for t in threads:
    t.start()

# Wait for all threads to finish
for t in threads:
    t.join()

print("All tasks done!")
