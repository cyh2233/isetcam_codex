import numpy as np

from isetcam.sensor import Sensor, sensor_jiggle, sensor_pixel_coord


def _simple_sensor(width: int = 3, height: int = 3) -> Sensor:
    volts = np.arange(width * height, dtype=float).reshape(height, width)
    s = Sensor(volts=volts, wave=np.array([500]), exposure_time=0.01)
    s.pixel_size = 1.0
    return s


def _shift(arr: np.ndarray, dx: int, dy: int, fill: float = 0) -> np.ndarray:
    h, w = arr.shape[:2]
    out = np.full_like(arr, fill)
    if abs(dx) < w and abs(dy) < h:
        if dx >= 0:
            src_x = slice(0, w - dx)
            dst_x = slice(dx, dx + (w - dx))
        else:
            src_x = slice(-dx, w)
            dst_x = slice(0, w + dx)

        if dy >= 0:
            src_y = slice(0, h - dy)
            dst_y = slice(dy, dy + (h - dy))
        else:
            src_y = slice(-dy, h)
            dst_y = slice(0, h + dy)

        out[dst_y, dst_x, ...] = arr[src_y, src_x, ...]
    return out


def test_sensor_jiggle_offsets_and_alignment():
    s = _simple_sensor(3, 3)
    dx, dy = 1, -1
    out = sensor_jiggle(s, dx, dy)

    expected = _shift(s.volts, dx, dy, fill=0)
    assert np.array_equal(out.volts, expected)

    x0, y0 = sensor_pixel_coord(s)
    x1, y1 = sensor_pixel_coord(out)
    assert np.allclose(x1, x0 + dx * s.pixel_size)
    assert np.allclose(y1, y0 + dy * s.pixel_size)


def test_sensor_jiggle_outside():
    s = _simple_sensor(2, 2)
    out = sensor_jiggle(s, 5, 0, fill=-1)
    assert np.array_equal(out.volts, np.full_like(s.volts, -1))
