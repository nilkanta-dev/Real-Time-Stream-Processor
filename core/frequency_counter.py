from collections import defaultdict

class FrequencyCounter:
    def __init__(self):
        self.freq = defaultdict(int)

    def add(self, item):
        self.freq[item] += 1

    def remove(self, item):
        if self.freq[item] > 1:
            self.freq[item] -= 1
        else:
            del self.freq[item]

    def get_counts(self):
        return dict(self.freq)

    def reset(self):
        self.freq.clear()
