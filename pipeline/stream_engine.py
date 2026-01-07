import time
from pipeline.event_queue import event_queue
from pipeline.window_manager import WindowManager
from core.heap_topk import TopKHeap
from core.bloom_rotation import RotatingBloom
from monitor.eps_meter import EPSMeter
from monitor.queue_health import queue_health
from core.burst_detector import BurstDetector
from core.alert_manager import AlertManager
from core.severity_engine import SeverityEngine
from core.config_loader import load_config
from core.event_log import EventLog



def run_engine():


    cfg = load_config()

    windows = {
    label: WindowManager(window_size=sec)
    for label, sec in cfg["windows"].items()
}


    detectors = {
    label: BurstDetector(
        growth_threshold=cfg["burst"]["growth_thresholds"][label],
        min_prev_count=cfg["burst"]["min_prev_count"],
    )
    for label in cfg["windows"]
}



    topk = TopKHeap(k=3)

    bloom = RotatingBloom(
    size=cfg["bloom"]["size"],
    hash_count=cfg["bloom"]["hash_count"],
    rotate_interval=cfg["bloom"]["rotate_interval"],
)
    alert_mgr = AlertManager(
    confirm_count=cfg["alerts"]["confirm_count"],
    cooldown=cfg["alerts"]["cooldown"],
)

    severity_engine = SeverityEngine(
    window_weights=cfg["severity"]["window_weights"],
    ttl=cfg["severity"]["ttl"],
)

    eps = EPSMeter()
    event_log = EventLog()


    print("Replaying historical events...")
    for offset, event in event_log.replay_from_offset():
        for w in windows.values():
            w.add_event(event)
        event_log.commit_offset(offset + 1)
    print("Consumer started. Waiting for events...\n")



    while True:
        BATCH_SIZE = 5
        batch = []

        while len(batch) < BATCH_SIZE:
            event = event_queue.get()
            batch.append(event)

        eps.record(len(batch))  # count events

        for event in batch:
            # time.sleep(0.02) to simulate consumer slow down
            if bloom.contains(event):
                continue
            bloom.add(event)

            for w in windows.values():
                w.add_event(event)

        print("\n=== REAL-TIME TRENDING ===")
        for label, w in windows.items():
            freqs = w.get_frequencies()
            topk.build(freqs)
            print(f"{label} Window Top 3:", topk.get_topk())


            bursts = detectors[label].detect(freqs)
            for b in bursts:
                alert = alert_mgr.process(label,b)
                if alert:
                    final = severity_engine.ingest(alert)
                    if final:
                        print(
                            f"{final['severity']} ALERT: {final['item']} "
                            f"(confidence={final['confidence']}, windows={final['windows']})"
                            )


        # show engine health
        size, maxsize, percent, status = queue_health()
        print(f"\nQueue: {size}/{maxsize}  ({percent}%)  Status: {status}")

        print(f"EPS: {eps.get_eps()} events/sec")

        print("=" * 60)

        event_queue.task_done()
        time.sleep(0.5)
