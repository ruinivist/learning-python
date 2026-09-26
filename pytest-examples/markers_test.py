import pytest


@pytest.mark.slow
def test_slow_marker():
    assert 2 + 2 == 4


@pytest.mark.serial
def test_serial_marker():
    assert "serial".upper() == "SERIAL"
