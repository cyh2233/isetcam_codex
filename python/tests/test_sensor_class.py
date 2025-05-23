import numpy as np
from isetcam.sensor import (
    Sensor,
    get_volts,
    set_volts,
    get_exposure_time,
    set_exposure_time,
    get_n_wave,
)


def test_sensor_accessors():
    wave = np.array([500, 510, 520])
    volts = np.ones((1, 1, 3))
    exposure_time = 0.01
    s = Sensor(volts=volts.copy(), wave=wave, exposure_time=exposure_time)

    assert get_n_wave(s) == 3
    assert np.allclose(get_volts(s), volts)
    assert get_exposure_time(s) == exposure_time

    new_volts = np.zeros_like(volts)
    set_volts(s, new_volts)
    assert np.allclose(get_volts(s), new_volts)

    new_exposure = 0.02
    set_exposure_time(s, new_exposure)
    assert get_exposure_time(s) == new_exposure
