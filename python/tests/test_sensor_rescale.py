import numpy as np
from scipy.ndimage import zoom as nd_zoom

from isetcam.sensor import Sensor, sensor_rescale


def test_sensor_rescale_basic():
    volts = np.arange(4, dtype=float).reshape(2, 2)
    s = Sensor(volts=volts, wave=np.array([550]), exposure_time=0.01)
    out = sensor_rescale(s, (4, 4), (4e-6, 4e-6))

    expected = nd_zoom(volts, (2, 2), order=1)
    assert np.allclose(out.volts, expected)
    assert out.volts.shape == (4, 4)
    assert np.array_equal(out.wave, s.wave)

    expected_px = (4e-6 / 4 + 4e-6 / 4) / 2.0
    assert np.isclose(out.pixel_size, expected_px)
