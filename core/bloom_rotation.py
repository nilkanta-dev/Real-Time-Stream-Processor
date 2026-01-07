import time
from core.bloom_filter import BloomFilter


class RotatingBloom:
    def __init__(self, size=50000, hash_count=6, rotate_interval=2):
        self.size = size
        self.hash_count = hash_count
        self.rotate_interval = rotate_interval

        self.active = BloomFilter(size, hash_count)
        self.old = BloomFilter(size, hash_count)
        self.last_rotation = time.time()

    def _rotate_if_needed(self):
        if time.time() - self.last_rotation > self.rotate_interval:
            self.old = self.active
            self.active = BloomFilter(self.size, self.hash_count)
            self.last_rotation = time.time()

    def contains(self, item):
        self._rotate_if_needed()
        return self.active.contains(item) or self.old.contains(item)

    def add(self, item):
        self._rotate_if_needed()
        self.active.add(item)
