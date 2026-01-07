from pipeline.burst_controller import BurstController
from pipeline.event_queue import event_queue
from core.event_log import EventLog
import threading
import time


def start_producer(batch_size=5, interval=0.2):

    items = [
        "apple", "banana", "carrot",
        "dog", "earphone", "fan",
        "glass", "hat", "ice", "jacket"
    ]

    burst = BurstController(
        items=items,
        burst_duration=15,
        burst_weight=0.8
    )

    event_log = EventLog()

    def run():
        while True:
            batch = []

            for _ in range(batch_size):
                event = burst.next_event()
                batch.append(event)
                event_log.append(event)

            for event in batch:
                event_queue.put(event)
                time.sleep(interval)#to prevent bursts.keep this outside of loop to see bursts

    threading.Thread(target=run, daemon=True).start()
