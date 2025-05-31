import numpy as np
from isetcam.sensor import Sensor, sensor_set, sensor_add_noise


def test_sensor_add_noise_dsnu():
    np.random.seed(0)
    volts = np.zeros((100, 100), dtype=float)
    s = Sensor(volts=volts.copy(), wave=np.array([550]), exposure_time=0.01)
    sensor_set(s, "gain_sd", 0.0)
    sensor_set(s, "offset_sd", 0.1)

    noisy, noise = sensor_add_noise(s)

    assert noisy.shape == volts.shape
    assert np.allclose(noisy - volts, noise)
    assert np.allclose(s.volts, noisy)
    assert abs(noise.mean()) < 5e-3
    assert abs(noise.var() - 0.01) < 5e-3


def test_sensor_add_noise_prnu():
    np.random.seed(1)
    volts = np.ones((100, 100), dtype=float)
    s = Sensor(volts=volts.copy(), wave=np.array([550]), exposure_time=0.01)
    sensor_set(s, "gain_sd", 10.0)
    sensor_set(s, "offset_sd", 0.0)

    noisy, noise = sensor_add_noise(s)

    assert abs(noise.mean()) < 5e-3
    assert abs(noise.var() - 0.01) < 5e-3


def test_sensor_add_noise_combined():
    np.random.seed(2)
    volts = np.full((50, 50), 2.0, dtype=float)
    s = Sensor(volts=volts.copy(), wave=np.array([550]), exposure_time=0.01)
    sensor_set(s, "gain_sd", 5.0)
    sensor_set(s, "offset_sd", 0.2)

    noisy, noise = sensor_add_noise(s)

    expected_var = 0.2 ** 2 + (0.05 * 2.0) ** 2
    assert abs(noise.mean()) < 1e-2
    assert abs(noise.var() - expected_var) < 5e-3

