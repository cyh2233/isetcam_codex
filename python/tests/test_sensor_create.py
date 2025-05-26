import numpy as np

from isetcam.sensor import sensor_create, Sensor


def test_sensor_create_default():
    s = sensor_create()
    assert isinstance(s, Sensor)
    assert s.exposure_time == 0.01
    assert hasattr(s, "qe")
    assert hasattr(s, "pixel_size")
    assert s.qe.size == s.wave.size


def test_sensor_create_custom_wave():
    wave = np.array([500, 510, 520])
    s = sensor_create(wave=wave)
    assert np.array_equal(s.wave, wave)
    assert s.qe.size == wave.size
