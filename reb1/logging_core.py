from __future__ import annotations
import time
import datetime as dt
from typing import Optional, Callable
import psutil
from .utils.csv_writer import CsvWriter
from .utils.timebase import Rate


def utc_iso() -> str:
    return dt.datetime.utcnow().replace(tzinfo=dt.timezone.utc).isoformat().replace("+00:00", "Z")


def run_logging(
    out_csv: str,
    hz: float,
    duration_s: float,
    host: str,
    source_name: str,
    device_index: int,
    policy_name: str,
    grid_gco2_per_kwh: float,
    sensor,
    note: str = "",
    cmd_vel_speed_supplier: Optional[Callable[[], Optional[float]]] = None,
) -> None:
    """
    Shared sampling loop:
      - psutil CPU util
      - source sensor read
      - optional cmd_vel speed supplier
      - exact CSV schema
    """
    writer = CsvWriter(out_csv)
    rate = Rate(hz)
    # Prime psutil measurement window
    psutil.cpu_percent(interval=None)
    end_time = time.time() + duration_s
    try:
        while time.time() <= end_time:
            dt_sec = rate.sleep()
            if hasattr(sensor, "step"):
                sensor.step(dt_sec)
            sample = sensor.read()

            # Attempt to pull fields generically
            gpu_util = getattr(sample, "gpu_util", None)
            soc_power_w = getattr(sample, "soc_power_w", None)
            gpu_power_w = getattr(sample, "gpu_power_w", None)
            cpu_power_w = getattr(sample, "cpu_power_w", None)
            temp_c = getattr(sample, "temp_c", None)
            cmd_speed = getattr(sample, "cmd_vel_speed", None)
            if cmd_vel_speed_supplier is not None:
                ext = cmd_vel_speed_supplier()
                if ext is not None:
                    cmd_speed = ext

            row = dict(
                timestamp=utc_iso(),
                host=host,
                source=source_name,
                device_index=device_index,
                policy_name=policy_name,
                hz=hz,
                cpu_util=round(psutil.cpu_percent(interval=None), 3),
                gpu_util=gpu_util if gpu_util is not None else "",
                soc_power_w=soc_power_w if soc_power_w is not None else "",
                gpu_power_w=gpu_power_w if gpu_power_w is not None else "",
                cpu_power_w=cpu_power_w if cpu_power_w is not None else "",
                temp_c=temp_c if temp_c is not None else "",
                cmd_vel_speed=cmd_speed if cmd_speed is not None else "",
                note=note,
            )
            writer.write_row(row)
    finally:
        writer.close()
