import time
#event per second meter
class EPSMeter:
    def __init__(self):
        self.count = 0
        self.start = time.time()

    def record(self, n=1):
        self.count += n

    def get_eps(self):
        elapsed = time.time() - self.start
        if elapsed == 0:
            return 0
        return round(self.count / elapsed, 2)
