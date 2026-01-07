import random
import time

class BurstController:
    def __init__(self, items, burst_duration=15, burst_weight=0.7):
        self.items = items
        self.burst_duration = burst_duration
        self.burst_weight = burst_weight

        self.current_burst = random.choice(items)
        self.last_switch = time.time()

    def _rotate_burst(self):
        if time.time() - self.last_switch > self.burst_duration:
            self.current_burst = random.choice(self.items)
            self.last_switch = time.time()

    def next_event(self):
        self._rotate_burst()

        if random.random() < self.burst_weight:
            return self.current_burst
        return random.choice(self.items)
