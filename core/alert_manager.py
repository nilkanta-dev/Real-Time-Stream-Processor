# core/alert_manager.py
import time
from collections import defaultdict

class AlertManager:
    def __init__(self, confirm_count=2, cooldown=10):
        self.confirm_count = confirm_count
        self.cooldown = cooldown

        self.burst_counts = defaultdict(int)
        self.last_alert_time = {}

    def process(self, window, burst):
        """
        burst: {item, growth, prev, current}
        """
        key = (window, burst["item"])
        now = time.time()

        # increment burst confirmation count
        self.burst_counts[key] += 1

        # cooldown check
        last_time = self.last_alert_time.get(key, 0)
        if now - last_time < self.cooldown:
            return None

        # confirmation check
        if self.burst_counts[key] >= self.confirm_count:
            self.last_alert_time[key] = now
            self.burst_counts[key] = 0  # reset after alert

            return {
                "window": window,
                "item": burst["item"],
                "growth": burst["growth"],
                "current": burst["current"],
            }

        return None
