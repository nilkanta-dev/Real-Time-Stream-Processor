
from collections import deque
import time
from core.frequency_counter import FrequencyCounter


class WindowManager:
    def __init__(self, window_size=5):
        self.window = deque()
        self.window_size = window_size
        self.counter = FrequencyCounter()

    def add_event(self, data):
        timestamp = time.time()
        self.window.append((timestamp, data))
        self.counter.add(data)
        self._evict_old()

    def _evict_old(self):
        now = time.time()
        while self.window and now - self.window[0][0] > self.window_size:
            _, old_data = self.window.popleft()
            self.counter.remove(old_data)

    def get_recent_events(self):
        return [data for (_, data) in self.window]

    def get_frequencies(self):
        return self.counter.get_counts()
