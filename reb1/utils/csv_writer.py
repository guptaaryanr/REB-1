from __future__ import annotations
import csv
import os
from typing import Dict

SCHEMA = [
    "timestamp",
    "host",
    "source",
    "device_index",
    "policy_name",
    "hz",
    "cpu_util",
    "gpu_util",
    "soc_power_w",
    "gpu_power_w",
    "cpu_power_w",
    "temp_c",
    "cmd_vel_speed",
    "note",
]


class CsvWriter:
    def __init__(self, path: str) -> None:
        self.path = path
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self._fh = open(path, "w", newline="")
        self._w = csv.DictWriter(self._fh, fieldnames=SCHEMA)
        self._w.writeheader()

    def write_row(self, row: Dict[str, object]) -> None:
        out: Dict[str, object] = {k: row.get(k, "") for k in SCHEMA}
        self._w.writerow(out)
        self._fh.flush()

    def close(self) -> None:
        try:
            self._fh.close()
        except Exception:
            pass
