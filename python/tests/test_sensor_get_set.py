import numpy as np

from isetcam.sensor import Sensor, sensor_get, sensor_set


def test_sensor_get_set():
    wave = np.array([500, 510, 520])
    volts = np.ones((2, 2, 3))
    s = Sensor(volts=volts.copy(), wave=wave, exposure_time=0.01, name="orig")

    assert np.allclose(sensor_get(s, " VOLTS"), volts)
    assert np.array_equal(sensor_get(s, " WAVE"), wave)
    assert sensor_get(s, "N WAVE") == 3
    assert sensor_get(s, "EXPOSURE TIME") == 0.01
    assert sensor_get(s, " NaMe") == "orig"

    new_volts = np.zeros_like(volts)
    sensor_set(s, " VolTs ", new_volts)
    assert np.allclose(sensor_get(s, "vOlTs"), new_volts)

    new_wave = np.array([400, 500])
    sensor_set(s, " wAvE", new_wave)
    assert np.array_equal(sensor_get(s, "WAVE"), new_wave)
    assert sensor_get(s, "N_WAVE") == len(new_wave)

    sensor_set(s, "Exposure_Time", 0.02)
    assert sensor_get(s, "ExPosure TiMe") == 0.02

    sensor_set(s, " NAME ", "new")
    assert sensor_get(s, " Name ") == "new"
