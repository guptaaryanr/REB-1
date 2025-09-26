from __future__ import annotations
import math
from typing import Optional
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

from reb1.logging_core import run_logging
from reb1.sensors.nvidia_smi import NvidiaSmiSensor, command_exists as nvsmi_exists
from reb1.sensors.demo import DemoSensor
from reb1.sensors.tegrastats import TegraStatsSensor, command_exists as tegra_exists
from reb1.utils.system_info import default_host


class PowerLoggerNode(Node):
    def __init__(self) -> None:
        super().__init__("reb1_power_logger")
        # Declare parameters
        self.declare_parameter("out", "reb1_ros.csv")
        self.declare_parameter("hz", 2.0)
        self.declare_parameter("duration_s", 60.0)
        self.declare_parameter("policy_name", "ros_policy")
        self.declare_parameter("source", "demo")
        self.declare_parameter("device_index", 0)
        self.declare_parameter("grid_gco2_per_kwh", 400.0)
        self.declare_parameter("note", "")

        self._cmd_vel_speed: Optional[float] = None
        try:
            self._sub = self.create_subscription(Twist, "/cmd_vel", self._on_twist, 10)
        except Exception as e:
            self.get_logger().warn(f"Failed to subscribe /cmd_vel: {e}")

    def _on_twist(self, msg: Twist) -> None:
        vx, vy, vz = msg.linear.x, msg.linear.y, msg.linear.z
        self._cmd_vel_speed = math.sqrt(vx * vx + vy * vy + vz * vz)

    def run(self) -> None:
        args = {
            p: self.get_parameter(p).get_parameter_value()._value
            for p in [
                "out",
                "hz",
                "duration_s",
                "policy_name",
                "source",
                "device_index",
                "grid_gco2_per_kwh",
                "note",
            ]
        }
        source = args["source"]
        device_index = int(args["device_index"])

        # Source selection with graceful handling
        if source == "nvidia_smi":
            if not nvsmi_exists():
                self.get_logger().warn("nvidia-smi not found; falling back to demo")
                sensor = DemoSensor(policy_name=args["policy_name"], seed=42)
                source_name = "demo"
            else:
                sensor = NvidiaSmiSensor(device_index=device_index)
                source_name = "nvidia_smi"
        elif source == "tegrastats":
            if not tegra_exists():
                self.get_logger().warn("tegrastats not found; falling back to demo")
                sensor = DemoSensor(policy_name=args["policy_name"], seed=42)
                source_name = "demo"
            else:
                sensor = TegraStatsSensor()
                source_name = "tegrastats"
        else:
            sensor = DemoSensor(
                policy_name=args["policy_name"], seed=42 if args["policy_name"] == "idle" else 1337
            )
            source_name = "demo"

        def supplier() -> Optional[float]:
            return self._cmd_vel_speed

        run_logging(
            out_csv=str(args["out"]),
            hz=float(args["hz"]),
            duration_s=float(args["duration_s"]),
            host=default_host(),
            source_name=source_name,
            device_index=device_index,
            policy_name=str(args["policy_name"]),
            grid_gco2_per_kwh=float(args["grid_gco2_per_kwh"]),
            sensor=sensor,
            note=str(args["note"]),
            cmd_vel_speed_supplier=supplier,
        )


def main() -> None:
    rclpy.init()
    node = PowerLoggerNode()
    try:
        node.run()
    finally:
        node.destroy_node()
        rclpy.shutdown()
