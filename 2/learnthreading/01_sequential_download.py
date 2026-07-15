"""
01 — The Problem: Python Is Normally "One Thing at a Time"

By default, Python does tasks one after another. It finishes the first task
completely before moving to the second. While waiting (e.g. for a "download"),
Python is just sitting there doing nothing.

Total time: 9 seconds (3 + 3 + 3), even though we could do all three at once.
"""
import time


def download_file(name):
    print(f"Downloading {name}...")
    time.sleep(3)              # pretend this takes 3 seconds
    print(f"{name} downloaded!")


download_file("file_1.txt")   # waits 3 seconds
download_file("file_2.txt")   # waits another 3 seconds
download_file("file_3.txt")   # waits another 3 seconds
print("All done!")
