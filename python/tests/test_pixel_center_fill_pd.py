import numpy as np

from isetcam.sensor import Sensor
from isetcam.pixel import pixel_center_fill_pd


def test_pixel_center_fill_pd_area_and_volts():
    s = Sensor(volts=np.ones((1, 1)), wave=np.array([550]), exposure_time=1.0)
    s.pixel_size = 2e-6

    pixel_center_fill_pd(s, 0.25)

    expected_side = np.sqrt(0.25) * s.pixel_size
    p = s.pixel
    assert np.isclose(p.width, expected_side)
    assert np.isclose(p.height, expected_side)
    assert np.isclose(p.fill_factor, 0.25)
    assert np.isclose(p.width * p.height, 0.25 * s.pixel_size**2)

    assert np.allclose(s.volts, np.full((1, 1), 0.25))


def test_pixel_center_fill_pd_voltage_scaling():
    s1 = Sensor(volts=np.ones((1, 1)), wave=np.array([550]), exposure_time=1.0)
    s1.pixel_size = 2e-6
    pixel_center_fill_pd(s1, 1.0)

    s2 = Sensor(volts=np.ones((1, 1)), wave=np.array([550]), exposure_time=1.0)
    s2.pixel_size = 2e-6
    pixel_center_fill_pd(s2, 0.5)

    assert np.allclose(s1.volts, np.full((1, 1), 1.0))
    assert np.allclose(s2.volts, np.full((1, 1), 0.5))
