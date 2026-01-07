from collections import deque
import time

#Just to have an idea on how sliding window works
class SlidingWindow:
    def __init__(self, window_size_seconds):
        self.window = deque()
        self.window_size = window_size_seconds

    def add(self, value):
        timestamp = time.time()
        self.window.append((timestamp, value))
        self._cleanup()

    def _cleanup(self):
        current_time = time.time()
        while self.window and current_time - self.window[0][0] > self.window_size:
            self.window.popleft()

    def get_values(self):
        return [v for (_, v) in self.window]


if __name__ == "__main__":
    w = SlidingWindow(window_size_seconds=5)

    for i in range(10):
        w.add(i)
        print("Window:", w.get_values())
        time.sleep(1)
