# Changelog

## [0.1.0] - 2025-09-25
Initial public release of **REB-1: ROS Energy Benchmark**.

- CLI fallback (`reb1.cli`) with `demo` and `nvidia-smi` sources.
- ROS 2 node (`ros_reb1/power_logger_node.py`) subscribing to `/cmd_vel`.
- Fixed CSV schema with power, utilization, and optional velocity columns.
- Deterministic demo source for reproducibility and CI tests.
- Micro-dataset (two 60s runs) and analysis notebook with bar chart + GIF.
- Unit tests + GitHub Actions CI (ROS not required).
- Documentation, JOSS-style paper draft, and project metadata files.
