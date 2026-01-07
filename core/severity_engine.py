# core/severity_engine.py
from collections import defaultdict
import time

class SeverityEngine:
    def __init__(self, window_weights=None, ttl=20):
        self.window_weights = window_weights or {
            "5s": 1,
            "15s": 2,
            "60s": 3,
        }
        self.ttl = ttl
        self.active = defaultdict(dict)

    def ingest(self, alert):
        """
        alert: {window, item, growth, current}
        """
        item = alert["item"]
        window = alert["window"]
        now = time.time()

        self.active[item][window] = {
            "growth": alert["growth"],
            "time": now,
        }

        return self._evaluate(item, now)

    def _evaluate(self, item, now):
        score = 0
        windows = []

        for w, data in list(self.active[item].items()):
            if now - data["time"] > self.ttl:
                del self.active[item][w]
                continue

            score += self.window_weights.get(w, 1)
            windows.append(w)

        if score >= 4:
            return {
                "item": item,
                "severity": "HIGH",
                "confidence": round(score / 6, 2),
                "windows": windows,
            }
        elif score >= 2:
            return {
                "item": item,
                "severity": "MEDIUM",
                "confidence": round(score / 6, 2),
                "windows": windows,
            }

        return None
