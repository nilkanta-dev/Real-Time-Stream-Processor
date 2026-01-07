import heapq

class TopKHeap:
    def __init__(self, k=3):
        self.k = k
        self.heap = []

    def build(self, freq_dict):
        self.heap = []

        for item, count in freq_dict.items():
            heapq.heappush(self.heap, (count, item))
            if len(self.heap) > self.k:
                heapq.heappop(self.heap)

    def get_topk(self):
        return sorted(self.heap, reverse=True)
