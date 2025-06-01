import numpy as np
from isetcam.sensor import Sensor, sensor_gain_offset


def test_sensor_gain_offset_basic():
    volts = np.array([[1.0, 2.0], [3.0, 4.0]])
    s = Sensor(volts=volts.copy(), wave=np.array([550]), exposure_time=0.01)
    sensor_gain_offset(s, gain=2.0, offset=-1.0)
    expected = volts * 2.0 - 1.0
    assert np.allclose(s.volts, expected)
