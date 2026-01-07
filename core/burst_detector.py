
class BurstDetector:
    def __init__(self, growth_threshold=3.0, min_prev_count=2):
        self.growth_threshold = growth_threshold
        self.min_prev_count = min_prev_count
        self.previous_state = {}

    def detect(self, current_freqs):
        """
        current_freqs: dict[item -> count]
        returns: list of burst events
        """
        bursts = []

        for item, current_count in current_freqs.items():
            prev_count = self.previous_state.get(item, 0)

            if prev_count >= self.min_prev_count:
                growth = current_count / prev_count
                if growth >= self.growth_threshold:
                    bursts.append({
                        "item": item,
                        "growth": round(growth, 2),
                        "prev": prev_count,
                        "current": current_count,
                    })

        # update state AFTER detection
        self.previous_state = current_freqs.copy()
        return bursts
