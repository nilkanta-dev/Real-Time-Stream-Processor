import mmh3
from bitarray import bitarray


class BloomFilter:
    def __init__(self, size=10000, hash_count=5):
        self.size = size
        self.hash_count = hash_count
        self.bit_array = bitarray(size)
        self.bit_array.setall(0)

    def _hashes(self, item):
        for i in range(self.hash_count):
            yield mmh3.hash(item, i) % self.size

    def add(self, item):
        for idx in self._hashes(item):
            self.bit_array[idx] = 1

    def contains(self, item):
        return all(self.bit_array[idx] for idx in self._hashes(item))
