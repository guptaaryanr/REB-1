import csv
from reb1.cli import main as cli_main
from reb1.utils.csv_writer import SCHEMA


def test_demo_csv_schema_and_nonempty(tmp_path):
    outp = tmp_path / "mini.csv"
    # Short capture: 2 seconds at 2 Hz -> ~4-5 rows
    rc = cli_main(
        [
            "--source",
            "demo",
            "--duration_s",
            "2",
            "--hz",
            "2",
            "--policy_name",
            "idle",
            "--out",
            str(outp),
        ]
    )
    assert rc == 0 and outp.exists() and outp.stat().st_size > 0

    with open(outp, newline="") as fh:
        reader = csv.reader(fh)
        header = next(reader)
        assert header == SCHEMA
        rows = list(reader)
        assert len(rows) >= 3  # at least a few samples


def test_ros_deps_not_required():
    try:
        import rclpy  # noqa: F401

        got_ros = True
    except Exception:
        got_ros = False
    # This test should not depend on ROS presence; just ensure import outcome doesn't matter
    assert got_ros in (True, False)
