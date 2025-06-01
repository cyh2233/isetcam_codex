import numpy as np
from isetcam.sensor import Sensor, sensor_roi


def _simple_sensor(width: int = 4, height: int = 4) -> Sensor:
    pattern = np.fromfunction(lambda y, x: (y % 2) * 2 + (x % 2), (height, width), dtype=int)
    return Sensor(volts=pattern.astype(float), wave=np.array([500]), exposure_time=0.01)


def test_sensor_roi_basic():
    s = _simple_sensor(4, 4)
    roi, rows, cols = sensor_roi(s, (1, 1, 2, 2))
    expected = s.volts[1:3, 1:3]
    assert np.array_equal(roi, expected)
    assert np.array_equal(rows, np.array([1, 2]))
    assert np.array_equal(cols, np.array([1, 2]))


def test_sensor_roi_clip_bounds():
    s = _simple_sensor(4, 4)
    roi, rows, cols = sensor_roi(s, (-1, -1, 3, 3))
    exp_rows = np.array([0, 0, 1])
    exp_cols = np.array([0, 0, 1])
    assert np.array_equal(rows, exp_rows)
    assert np.array_equal(cols, exp_cols)
    assert np.array_equal(roi, s.volts[np.ix_(exp_rows, exp_cols)])


def test_sensor_roi_bad_size():
    s = _simple_sensor(2, 2)
    with np.testing.assert_raises(ValueError):
        sensor_roi(s, (0, 0, 0, 1))
    with np.testing.assert_raises(ValueError):
        sensor_roi(s, (0, 0, 1, 0))
