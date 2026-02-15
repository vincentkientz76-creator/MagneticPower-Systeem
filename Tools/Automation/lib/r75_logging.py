import csv
import os
import time
from typing import Dict

LOG_FIELDS = ["timestamp", "stage", "level", "sku", "message"]

class R75Logger:
    def __init__(self, log_path: str):
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        self._f = open(log_path, "w", newline="", encoding="utf-8")
        self._w = csv.DictWriter(self._f, fieldnames=LOG_FIELDS)
        self._w.writeheader()
        self.metrics: Dict[str, int] = {
            "total_input": 0,
            "matched_bb_manual": 0,
            "missing_bb_manual": 0,
            "errors": 0,
            "keep_count": 0,
            "review_count": 0,
            "drop_count": 0,
        }

    def log(self, stage: str, level: str, sku: str, message: str) -> None:
        self._w.writerow({
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "stage": stage,
            "level": level,
            "sku": sku,
            "message": message,
        })

    def close(self) -> None:
        self._f.flush()
        self._f.close()
