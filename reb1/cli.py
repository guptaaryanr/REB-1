from __future__ import annotations
import argparse
import sys
from typing import Optional
from .logging_core import run_logging
from .utils.system_info import default_host
from .sensors import nvidia_smi as nvsmi
from .sensors import demo as demo_src


def parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="REB-1 CLI power logger (ROS-optional)")
    p.add_argument("--out", required=True, help="Output CSV path")
    p.add_argument("--hz", type=float, default=2.0, help="Sampling frequency (Hz)")
    p.add_argument("--duration_s", type=float, default=60.0, help="Duration seconds")
    p.add_argument("--policy_name", type=str, default="idle")
    p.add_argument("--source", type=str, choices=["nvidia_smi", "demo"], default="demo")
    p.add_argument("--device_index", type=int, default=0)
    p.add_argument("--grid_gco2_per_kwh", type=float, default=400.0)
    p.add_argument("--note", type=str, default="")
    return p.parse_args(argv)


def main(argv: Optional[list[str]] = None) -> int:
    args = parse_args(argv)
    host = default_host()

    # Select source
    if args.source == "nvidia_smi":
        if not nvsmi.command_exists():
            print(
                "[reb1] WARNING: nvidia-smi not found; use '--source demo' on WSL if needed.",
                file=sys.stderr,
            )
            print("[reb1] Falling back to demo source for this run.", file=sys.stderr)
            sensor = demo_src.DemoSensor(policy_name=args.policy_name, seed=42)
            source_name = "demo"
        else:
            sensor = nvsmi.NvidiaSmiSensor(device_index=args.device_index)
            source_name = "nvidia_smi"
    else:
        sensor = demo_src.DemoSensor(
            policy_name=args.policy_name, seed=42 if args.policy_name == "idle" else 1337
        )
        source_name = "demo"

    run_logging(
        out_csv=args.out,
        hz=float(args.hz),
        duration_s=float(args.duration_s),
        host=host,
        source_name=source_name,
        device_index=int(args.device_index),
        policy_name=args.policy_name,
        grid_gco2_per_kwh=float(args.grid_gco2_per_kwh),
        sensor=sensor,
        note=args.note,
        cmd_vel_speed_supplier=None,  # no ROS here
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
