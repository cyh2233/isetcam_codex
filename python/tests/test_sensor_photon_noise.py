import numpy as np
from isetcam.sensor import Sensor, sensor_photon_noise


def test_sensor_photon_noise_gaussian():
    np.random.seed(0)
    volts = np.full((100, 100), 20.0, dtype=float)
    s = Sensor(volts=volts.copy(), wave=np.array([550]), exposure_time=0.01)
    noisy, noise = sensor_photon_noise(s)

    assert noisy.shape == volts.shape
    assert np.allclose(noisy - volts, noise)
    assert np.allclose(s.volts, noisy)
    assert abs(noise.mean()) < 0.1
    assert abs(noise.var() - 20.0) < 2.0


def test_sensor_photon_noise_poisson():
    np.random.seed(1)
    volts = np.full((100, 100), 5.0, dtype=float)
    s = Sensor(volts=volts.copy(), wave=np.array([550]), exposure_time=0.01)
    noisy, noise = sensor_photon_noise(s)

    assert np.allclose(s.volts, noisy)
    assert abs(noisy.mean() - 5.0) < 0.1
    assert abs(noise.mean()) < 0.1
    assert abs(noise.var() - 5.0) < 1.0
