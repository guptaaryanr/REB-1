from __future__ import annotations
import shutil
import subprocess
import re
from dataclasses import dataclass
from typing import Optional


@dataclass
class Sample:
    soc_power_w: Optional[float]
    gpu_power_w: Optional[float]
    gpu_util: Optional[float]
    temp_c: Optional[float]


def command_exists() -> bool:
    return shutil.which("tegrastats") is not None


# Example snippet contains: "RAM 1234/4096MB ... CPU@34C GPU@36C AO@33C thermal@35.5C POM_5V_IN 3000mW"
def parse_once(blob: str) -> Sample:
    def grab(pattern: str) -> Optional[float]:
        m = re.search(pattern, blob)
        if not m:
            return None
        try:
            return float(m.group(1))
        except Exception:
            return None

    soc_mw = grab(r"POM_5V_IN\s+([0-9.]+)mW")
    gpu_util = grab(r"GR3D_FREQ\s+([0-9.]+)%")
    gpu_pw = grab(r"GPU_PWR\s+([0-9.]+)mW")
    temp = grab(r"GPU@([0-9.]+)C") or grab(r"thermal@([0-9.]+)C")
    return Sample(
        soc_power_w=(soc_mw / 1000.0 if soc_mw is not None else None),
        gpu_power_w=(gpu_pw / 1000.0 if gpu_pw is not None else None),
        gpu_util=gpu_util,
        temp_c=temp,
    )


class TegraStatsSensor:
    def read(self) -> Sample:
        if not command_exists():
            return Sample(None, None, None, None)
        try:
            out = subprocess.check_output(
                ["tegrastats", "--interval", "1000", "--count", "1"], text=True
            )
            return parse_once(out)
        except Exception:
            return Sample(None, None, None, None)
