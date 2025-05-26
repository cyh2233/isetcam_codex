import numpy as np
import pytest

from isetcam.sensor import Sensor, sensor_crop


def _simple_sensor(width: int = 4, height: int = 4) -> Sensor:
    # create a simple repeating 2x2 CFA pattern
    pattern = np.fromfunction(lambda y, x: (y % 2) * 2 + (x % 2), (height, width), dtype=int)
    return Sensor(volts=pattern.astype(float), wave=np.array([500]), exposure_time=0.01)


def test_sensor_crop_basic():
    s = _simple_sensor(4, 4)
    out = sensor_crop(s, (0, 0, 2, 2))
    expected = s.volts[0:2, 0:2]
    assert np.array_equal(out.volts, expected)
    assert np.array_equal(out.wave, s.wave)
    assert out.crop_rect == (0, 0, 2, 2)
    assert out.full_size == (4, 4)


def test_sensor_crop_alignment_error():
    s = _simple_sensor(4, 4)
    with pytest.raises(ValueError):
        sensor_crop(s, (1, 0, 2, 2))
    with pytest.raises(ValueError):
        sensor_crop(s, (0, 0, 3, 2))

