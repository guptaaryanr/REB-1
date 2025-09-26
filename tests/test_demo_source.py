from reb1.sensors.demo import DemoSensor


def test_demo_idle_determinism():
    s1 = DemoSensor("idle", seed=42)
    s2 = DemoSensor("idle", seed=42)
    s1.step(0.5)
    s2.step(0.5)
    a = s1.read()
    b = s2.read()
    assert a.soc_power_w == b.soc_power_w
    assert a.gpu_power_w == b.gpu_power_w
    assert a.gpu_util == b.gpu_util
    assert a.temp_c == b.temp_c
    assert a.cmd_vel_speed == b.cmd_vel_speed


def test_demo_work_has_speed():
    s = DemoSensor("workload", seed=1337)
    s.step(1.0)
    x = s.read()
    assert x.cmd_vel_speed is not None and x.cmd_vel_speed >= 0.0
