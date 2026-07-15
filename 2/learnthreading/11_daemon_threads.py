"""
11 — Daemon Threads: Background Workers That Auto-Stop

By default, Python will NOT exit until all threads have finished.
Sometimes you want a background thread that runs forever (like a
sensor polling loop) and should automatically stop when the main
program ends.

That's what daemon=True is for.

Without daemon=True, this program would run forever because the
while True thread never stops.
"""
import threading
import time


def background_sensor():
    while True:
        print("Reading sensor...")
        time.sleep(1)


# daemon=True — this thread dies automatically when the main program exits
t = threading.Thread(target=background_sensor, daemon=True)
t.start()

# Main program does its work
print("Main program running...")
time.sleep(3)
print("Main program done. Exiting.")
# The daemon thread is automatically killed here — no need to stop it manually
