import numpy as np
from isetcam.sensor import Sensor, sensor_vignetting


def test_sensor_vignetting_unity():
    volts = np.zeros((3, 3), dtype=float)
    s = Sensor(volts=volts.copy(), wave=np.array([550]), exposure_time=0.01)

    sensor_vignetting(s)

    assert hasattr(s, "etendue")
    assert np.allclose(s.etendue, np.ones_like(volts))
