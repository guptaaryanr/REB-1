from __future__ import annotations
import math
import random
from dataclasses import dataclass
from typing import Optional


@dataclass
class Sample:
    soc_power_w: float
    gpu_power_w: float
    gpu_util: float
    temp_c: float
    cmd_vel_speed: Optional[float] = None


class DemoSensor:
    """
    Deterministic synthetic traces:
      - 'idle': low, mildly wavy
      - 'workload': higher baseline + activity pulse
    Seed controls determinism across runs.
    """

    def __init__(self, policy_name: str = "idle", seed: int = 42) -> None:
        self.t = 0.0
        self.dt = 0.0
        self.policy = policy_name
        random.seed(seed)
        self._phase = random.random() * math.pi

    def step(self, dt: float) -> None:
        self.dt = dt
        self.t += dt

    def read(self) -> Sample:
        # Base signals
        if self.policy == "idle":
            base = 12.0
            gpu = 5.0
            util = 3.0 + 0.3 * math.sin(0.3 * self.t + self._phase)
            temp = 40.0 + 0.05 * self.t
            speed = None
        else:
            base = 40.0 + 5.0 * math.sin(0.4 * self.t + self._phase)
            gpu = 30.0 + 5.0 * math.sin(0.8 * self.t + 0.5 * self._phase)
            util = 35.0 + 5.0 * math.sin(0.5 * self.t + 0.2 * self._phase)
            temp = 55.0 + 0.2 * self.t
            speed = 0.3 + 0.3 * max(0.0, math.sin(0.2 * self.t + 0.7 * self._phase))
        return Sample(
            soc_power_w=round(base, 3),
            gpu_power_w=round(gpu, 3),
            gpu_util=round(util, 3),
            temp_c=round(temp, 3),
            cmd_vel_speed=(round(speed, 3) if speed is not None else None),
        )
