---
title: "REB-1: ROS Energy Benchmark"
tags:
  - ROS 2
  - energy
  - benchmarking
  - reproducibility
authors:
  - name: Aryan Gupta
    orcid: 0009-0001-8179-5145
    affiliation: 1
affiliations:
  - name: Independent Researcher
    index: 1
date: 2025-09-25
bibliography: paper.bib
---

# Summary
REB-1 is a minimal, ROS 2–friendly energy micro-benchmark and power logger. It samples
GPU/SoC power via `nvidia-smi` or (optionally) `tegrastats`, writes tidy CSVs with a fixed schema,
and overlays `/cmd_vel` activity when available. A pure-Python CLI mirrors the ROS node so users
without ROS can still generate reproducible datasets.

# Statement of Need
Energy and carbon are increasingly important in robotics. ROS 2 users lack a simple,
cross-platform logger to capture watts over time and relate them to robot activity.
REB-1 provides a tiny, reproducible benchmark and analysis pipeline with minimal dependencies.
While tools exist for latency [@ros2_tracing] and throughput benchmarking [@ros2_benchmark],
no portable, ROS-compatible benchmark currently addresses the energy and CO₂ dimension.

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

# Related Work
Several projects touch adjacent areas but do not cover REB-1's scope:

- **ros2_tracing** instruments ROS 2 middleware with LTTng to analyze latency and scheduling [@ros2_tracing].
- **ros2_benchmark** (including the NVIDIA Isaac ROS Benchmark suite) evaluates throughput and performance of ROS 2 pipelines [@ros2_benchmark].
- **RobotPerf** provides robotics performance benchmarks across platforms, focusing on algorithmic throughput and latency rather than energy [@robotperf].
- **CodeCarbon** estimates energy and CO₂ for general machine learning workloads, but is not ROS-aware and does not integrate with robot activity topics [@codecarbon].
- **Jetson-specific tools** such as `tegrastats` and `jtop/jetson_stats` expose device telemetry [@tegrastats; @jtop], but they are platform-specific, lack a unified CSV schema, and do not convert Wh to CO₂.

In contrast, REB-1 uniquely provides a portable, CLI-first yet ROS-compatible micro-benchmark with a fixed CSV schema, deterministic demo workloads, a reproducible dataset, and an analysis notebook converting Wh to grams CO₂. It fills the energy/climate gap in ROS benchmarking alongside existing latency and throughput tools.

# Acknowledgements
Thanks to the ROS and open-source communities.

# References
