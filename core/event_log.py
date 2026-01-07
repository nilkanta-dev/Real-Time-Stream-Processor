import json
import os
import time

class EventLog:
    def __init__(self, path="data/logs/events.log", offset_path="data/offset.txt"):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        os.makedirs(os.path.dirname(offset_path), exist_ok=True)
        self.path = path
        self.offset_path = offset_path

    def append(self, event):
        record = {
            "event": event,
            "ts": time.time()
        }
        with open(self.path, "a") as f:
            f.write(json.dumps(record) + "\n")

    def get_offset(self):
        if not os.path.exists(self.offset_path):
            return 0
        with open(self.offset_path, "r") as f:
            content = f.read().strip()
            return int(content) if content else 0

    def commit_offset(self, offset):
        with open(self.offset_path, "w") as f:
            f.write(str(offset))

    def replay_from_offset(self):
        start = self.get_offset()
        with open(self.path, "r") as f:
            for i, line in enumerate(f):
                if i >= start:
                    yield i, json.loads(line)["event"]
