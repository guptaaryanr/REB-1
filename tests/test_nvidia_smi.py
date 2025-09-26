from reb1.sensors.nvidia_smi import parse_line


def test_parse_line_basic():
    pw, util = parse_line("35.21, 12")
    assert abs(pw - 35.21) < 1e-6
    assert abs(util - 12.0) < 1e-6


def test_parse_line_spaces_and_noise():
    pw, util = parse_line("  70.0 ,  99  ")
    assert pw == 70.0 and util == 99.0
    pw2, util2 = parse_line("N/A, N/A")
    assert pw2 is None and util2 is None
