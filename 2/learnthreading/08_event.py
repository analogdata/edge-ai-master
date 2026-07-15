"""
08 — threading.Event(): One Thread Signals Another

Sometimes one thread needs to wait for another thread to finish something
before it starts working. An Event is like a green light:

  - Event starts as "red light" (not set)
  - e.wait()  — pause here until the light turns green
  - e.set()   — turn on the green light

All threads waiting on the event will proceed once set() is called.
"""
import threading
import time

# Create an event (starts as "red light" — not set)
ready_event = threading.Event()


def setup_worker():
    print("Setting up... please wait")
    time.sleep(3)              # simulates setup taking time
    print("Setup complete!")
    ready_event.set()          # turn on the green light


def main_worker():
    print("Main worker waiting for setup...")
    ready_event.wait()         # pause here until the event is set
    print("Setup is done! Main worker starting now.")


t1 = threading.Thread(target=setup_worker)
t2 = threading.Thread(target=main_worker)

t2.start()   # starts waiting immediately
t1.start()   # starts doing setup

t1.join()
t2.join()
