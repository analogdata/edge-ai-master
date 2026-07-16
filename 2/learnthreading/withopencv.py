import threading
import queue
import cv2
import time

QUEUE_MAXSIZE = 5  # don't let the buffer grow unbounded


def producer(cap, frame_queue):
    """Captures frames and puts them in the queue."""
    while True:
        ret, frame = cap.read()
        if not ret:
            frame_queue.put(None)  # sentinel: signal end of stream
            break
        try:
            frame_queue.put_nowait(frame)   # non-blocking; drop frame if queue is full
        except queue.Full:
            pass  # acceptable: drop stale frames rather than accumulate lag


def consumer(frame_queue, display_queue):
    """Reads frames from the queue and runs inference."""
    while True:
        frame = frame_queue.get()           # blocks until a frame is available
        if frame is None:                   # sentinel: producer is done
            display_queue.put(None)
            break
        # Simulate inference here (e.g. model.predict(frame))
        display_queue.put(frame)            # main thread will display it
        frame_queue.task_done()


cap = cv2.VideoCapture(1)
frame_queue = queue.Queue(maxsize=QUEUE_MAXSIZE)
display_queue = queue.Queue(maxsize=QUEUE_MAXSIZE)

t_producer = threading.Thread(target=producer, args=(cap, frame_queue), daemon=True)
t_consumer = threading.Thread(target=consumer, args=(frame_queue, display_queue), daemon=True)

t_producer.start()
t_consumer.start()

# Main thread handles GUI (cv2.imshow must run on main thread on macOS)
while True:
    frame = display_queue.get()
    if frame is None:
        break
    cv2.imshow("Frame", frame)
    time.sleep(2)  # small delay to avoid overwhelming the display thread
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()