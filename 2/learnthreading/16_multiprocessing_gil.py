"""
16 — multiprocessing: Bypassing the GIL for CPU-Bound Inference

Python's Global Interpreter Lock (GIL) means that even with multiple
threads, only one thread executes Python bytecode at any given moment.
For I/O-bound work (waiting for a camera), threading works fine — the
GIL is released while waiting. But for CPU-bound work (heavy NumPy
operations, model inference in pure Python), multiple threads still
only use one CPU core effectively.

Solution: multiprocessing — spawns separate OS processes (each with
its own GIL), enabling true parallel CPU use on multi-core devices.

threading vs multiprocessing — decision guide:
  Camera capture (I/O wait)         → threading (GIL released during I/O)
  Serial/network data ingestion     → threading
  Heavy Python CPU inference        → multiprocessing
  NumPy-intensive pre/post-processing → multiprocessing (or vectorise)
  TFLite/ONNX inference (C-based)   → benchmark both before deciding

Note: multiprocessing has real overhead — process spawning time,
inter-process serialisation (pickling) of frames, separate memory
spaces. For a Pi with 1-2GB RAM, spawning many worker processes
is expensive. The right choice depends on profiling, not intuition.
"""
import multiprocessing as mp
import time


def cpu_intensive_task(worker_id, num_iterations=5_000_000):
    """Simulates heavy CPU-bound computation.

    In real code this could be:
      - Running a pure-Python inference loop
      - Heavy NumPy processing without vectorisation
      - Image processing in pure Python (not using cv2/NumPy)
    """
    total = 0
    for i in range(num_iterations):
        total += i * i
    return worker_id, total


def worker_process(input_q, output_q):
    """Worker process that receives tasks and returns results.

    Each process has its own GIL, so multiple processes can truly
    run in parallel on multiple CPU cores.
    """
    while True:
        task = input_q.get()
        if task is None:  # sentinel — stop the worker
            break
        worker_id, result = cpu_intensive_task(task)
        output_q.put((worker_id, result))


if __name__ == "__main__":
    input_q = mp.Queue(maxsize=4)
    output_q = mp.Queue(maxsize=4)

    # Start 2 worker processes — each has its own GIL
    workers = []
    for _ in range(2):
        p = mp.Process(target=worker_process, args=(input_q, output_q), daemon=True)
        p.start()
        workers.append(p)

    # Send tasks to workers
    num_tasks = 4
    for i in range(num_tasks):
        input_q.put(i)

    # Collect results
    results = []
    for _ in range(num_tasks):
        worker_id, result = output_q.get()
        results.append((worker_id, result))
        print(f"  Worker {worker_id} finished, result: {result}")

    # Send stop sentinels and clean up
    for _ in range(len(workers)):
        input_q.put(None)
    for p in workers:
        p.join()

    print(f"\nAll {num_tasks} tasks completed using {len(workers)} processes.")
    print("Each process ran on its own CPU core with its own GIL.")
