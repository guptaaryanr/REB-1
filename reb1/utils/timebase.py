from __future__ import annotations
import time


class Rate:
    def __init__(self, hz: float) -> None:
        self.period = 1.0 / float(hz)
        self._last = time.perf_counter()

    def sleep(self) -> float:
        now = time.perf_counter()
        elapsed = now - self._last
        delay = max(0.0, self.period - elapsed)
        if delay > 0:
            time.sleep(delay)
        now2 = time.perf_counter()
        dt = now2 - self._last
        self._last = now2
        return dt
