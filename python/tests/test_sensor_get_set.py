import numpy as np

from isetcam.sensor import Sensor, sensor_get, sensor_set


def test_sensor_get_set():
    wave = np.array([500, 510, 520])
    volts = np.ones((2, 2, 3))
    s = Sensor(volts=volts.copy(), wave=wave, exposure_time=0.01, name="orig")

    assert np.allclose(sensor_get(s, "volts"), volts)
    assert np.array_equal(sensor_get(s, "wave"), wave)
    assert sensor_get(s, "n wave") == 3
    assert sensor_get(s, "exposure time") == 0.01
    assert sensor_get(s, "name") == "orig"

    new_volts = np.zeros_like(volts)
    sensor_set(s, "volts", new_volts)
    assert np.allclose(sensor_get(s, "volts"), new_volts)

    new_wave = np.array([400, 500])
    sensor_set(s, "wave", new_wave)
    assert np.array_equal(sensor_get(s, "wave"), new_wave)
    assert sensor_get(s, "n_wave") == len(new_wave)

    sensor_set(s, "exposure_time", 0.02)
    assert sensor_get(s, "exposure time") == 0.02

    sensor_set(s, "name", "new")
    assert sensor_get(s, "name") == "new"
