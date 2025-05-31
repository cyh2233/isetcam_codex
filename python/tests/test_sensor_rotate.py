import numpy as np
from scipy.ndimage import rotate as nd_rotate

from isetcam.sensor import Sensor, sensor_rotate


def _simple_sensor(width: int = 3, height: int = 3) -> Sensor:
    volts = np.arange(width * height, dtype=float).reshape(height, width)
    return Sensor(volts=volts, wave=np.array([500]), exposure_time=0.01, name="simple")


def test_sensor_rotate_90():
    s = _simple_sensor(2, 3)
    out = sensor_rotate(s, 90)
    expected = np.rot90(s.volts, axes=(0, 1))
    assert np.array_equal(out.volts, expected)
    assert np.array_equal(out.wave, s.wave)
    assert out.name == s.name


def test_sensor_rotate_general():
    s = _simple_sensor(3, 3)
    angle = 30
    out = sensor_rotate(s, angle, fill=-1)
    expected = nd_rotate(
        s.volts,
        angle,
        axes=(1, 0),
        reshape=True,
        order=1,
        mode="constant",
        cval=-1,
    )
    assert np.allclose(out.volts, expected)
    assert np.array_equal(out.wave, s.wave)
    assert out.name == s.name
