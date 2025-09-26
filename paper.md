title: "REB-1: ROS Energy Benchmark"
authors:
  - name: Aryan Gupta
    orcid: 0009-0001-8179-5145
date: 2025-09-25
bibliography: []

# Summary
REB-1 is a minimal, ROS 2–friendly energy micro-benchmark and power logger. It samples
GPU/SoC power via `nvidia-smi` or (optionally) `tegrastats`, writes tidy CSVs with a fixed schema,
and overlays `/cmd_vel` activity when available. A pure-Python CLI mirrors the ROS node so users
without ROS can still generate reproducible datasets.

# Statement of Need
Energy and carbon are increasingly important in robotics. ROS 2 users lack a simple,
cross-platform logger to capture watts over time and relate them to robot activity.
REB-1 provides a tiny, reproducible benchmark and analysis pipeline with minimal dependencies.

# Positioning
REB-1 complements existing ROS benchmarking tools rather than replacing them. Whereas **ros2_tracing**
targets latency/scheduling analysis and **ros2_benchmark** focuses on throughput performance,
**REB-1** emphasizes the energy and carbon dimension by logging watts over time, integrating Wh,
and converting to grams CO₂. Together, these tools cover latency, throughput, and energy—three
orthogonal axes of system evaluation.

# Implementation
Sources:
- `nvidia_smi`: parses `nvidia-smi --query-gpu=power.draw,utilization.gpu --format=csv,noheader,nounits`
- `demo`: deterministic synthetic traces for reproducible tests/demos
- `tegrastats`: optional Jetson parser used only if the command exists

CSV schema (exact):  
`timestamp,host,source,device_index,policy_name,hz,cpu_util,gpu_util,soc_power_w,gpu_power_w,cpu_power_w,temp_c,cmd_vel_speed,note`

The ROS 2 node (`rclpy`) subscribes to `/cmd_vel` (`geometry_msgs/Twist`) and computes
`cmd_vel_speed = sqrt(vx^2 + vy^2 + vz^2)`. CPU util is sampled via `psutil`. The CLI shares the same
core logging loop and runs without ROS.

# Validation
We include a micro-dataset with two 60-second runs (`idle`, `workload`) at 2 Hz using the demo source
and an analysis notebook that computes energy (Wh), converts to grams CO₂, overlays activity on power,
renders a bar chart (PNG), and exports a short GIF.

# Reuse Potential
REB-1 is a foundation for comparing policies, kernels, or middleware configurations on energy.
It is lightweight, WSL-first, and ROS-optional—useful for CI/CD and educational labs.

# Limitations
- `nvidia-smi` covers NVIDIA GPUs; CPU package power is not directly measured.
- `tegrastats` support is best-effort and only used if present.
- Energy integration uses available power channels; SoC power preferred, GPU as fallback.

# Acknowledgements
Thanks to the ROS and open-source communities.

# References
- NVIDIA System Management Interface (nvidia-smi) documentation
- psutil documentation
- pandas, numpy, matplotlib, imageio documentation
- ROS 2 `rclpy` and `geometry_msgs` documentation
