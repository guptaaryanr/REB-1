from __future__ import annotations
import shutil
import subprocess
import re
from dataclasses import dataclass
from typing import Optional, Tuple

CSV_NOHEADER_NOUNITS = ["--query-gpu=power.draw,utilization.gpu", "--format=csv,noheader,nounits"]


@dataclass
class Sample:
    gpu_power_w: Optional[float]
    gpu_util: Optional[float]
    temp_c: Optional[float] = None
    soc_power_w: Optional[float] = None  # unknown from nvidia-smi
    cpu_power_w: Optional[float] = None  # unknown here


def command_exists() -> bool:
    return shutil.which("nvidia-smi") is not None


def parse_line(line: str) -> Tuple[Optional[float], Optional[float]]:
    """
    Parse a single CSV line like: "35.21, 12"
    Returns (gpu_power_w, gpu_util)
    Robust to spaces; ignores units due to 'nounits'.
    """
    parts = [p.strip() for p in line.strip().split(",")]
    if len(parts) < 2:
        return (None, None)
    try:
        pw = float(re.sub(r"[^0-9.+-]", "", parts[0]))
    except ValueError:
        pw = None
    try:
        util = float(re.sub(r"[^0-9.+-]", "", parts[1]))
    except ValueError:
        util = None
    return (pw, util)


class NvidiaSmiSensor:
    """Queries nvidia-smi for power + utilization. One-shot per sample."""

    def __init__(self, device_index: int = 0) -> None:
        self.device_index = int(device_index)

    def read(self) -> Sample:
        if not command_exists():
            return Sample(gpu_power_w=None, gpu_util=None)
        try:
            # Query all GPUs; pick device_index-th line for robustness
            out = subprocess.check_output(
                ["nvidia-smi"] + CSV_NOHEADER_NOUNITS, stderr=subprocess.STDOUT, text=True
            )
            lines = [ln for ln in out.strip().splitlines() if ln.strip()]
            if not lines or self.device_index >= len(lines):
                return Sample(gpu_power_w=None, gpu_util=None)
            pw, util = parse_line(lines[self.device_index])
            return Sample(gpu_power_w=pw, gpu_util=util)
        except Exception:
            return Sample(gpu_power_w=None, gpu_util=None)
