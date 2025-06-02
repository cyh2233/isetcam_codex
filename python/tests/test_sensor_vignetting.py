import numpy as np
from isetcam.sensor import Sensor, sensor_vignetting


def test_sensor_vignetting_unity():
    volts = np.zeros((3, 3), dtype=float)
    s = Sensor(volts=volts.copy(), wave=np.array([550]), exposure_time=0.01)

    sensor_vignetting(s)

    assert hasattr(s, "etendue")
    assert np.allclose(s.etendue, np.ones_like(volts))


def test_sensor_vignetting_microlens_improves():
    volts = np.zeros((5, 5), dtype=float)
    s = Sensor(volts=volts.copy(), wave=np.array([550]), exposure_time=0.01)
    s.pixel_size = 1e-6
    s.microlens_f_number = 2.8

    sensor_vignetting(s, 1)
    bare = s.etendue.copy()

    sensor_vignetting(s, "microlens")
    ml = s.etendue.copy()

    assert ml.shape == bare.shape
    assert ml[2, 2] >= bare[2, 2]
    assert ml[0, 0] >= bare[0, 0]
    assert np.all(ml <= 1.0)


def test_sensor_vignetting_numeric_flags():
    volts = np.zeros((3, 3), dtype=float)
    s = Sensor(volts=volts.copy(), wave=np.array([550]), exposure_time=0.01)

    sensor_vignetting(s, 2)
    et1 = s.etendue.copy()

    sensor_vignetting(s, 3)
    et2 = s.etendue.copy()

    assert np.allclose(et1, et2)
