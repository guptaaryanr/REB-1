# REB-1: ROS Energy Benchmark

**REB-1** is a ROS 2–friendly micro-benchmark and power/thermals logger that:
- samples power/utilization from `nvidia-smi` (WSL2-friendly) or a deterministic demo generator,
- writes **tidy CSVs** with a fixed schema,
- optionally overlays a ROS topic (`/cmd_vel`) activity,
- computes **energy (Wh)** and converts to **grams CO₂** (configurable grid factor),
- includes a tiny reproducible dataset + analysis notebook (plots + a GIF),
- ships tests + GitHub Actions CI that run **without ROS installed**.

Works great on **Ubuntu 22.04** under **WSL2** with Python 3.10. ROS 2 Humble is optional.

---

## Quickstart (WSL2, no ROS)

```bash
# 1) Create venv
python3.10 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip

# 2) Install REB-1 (editable dev install)
pip install -e ".[dev]"
```

---

## Prior art & scope

REB-1 is deliberately minimal. It complements but does not replace existing ROS benchmarking tools:

- **ros2_tracing**: targets *latency and scheduling analysis* by instrumenting the ROS 2 middleware with LTTng.  
- **ros2_benchmark**: targets *throughput and performance* benchmarking of ROS 2 pipelines.  
- **REB-1**: targets *energy and carbon impact* by logging watts over time, computing Wh, and converting to CO₂.

In short: **ros2_tracing ≈ latency**, **ros2_benchmark ≈ throughput**, **REB-1 ≈ power/Wh→CO₂**. They are complementary and can be used together.
