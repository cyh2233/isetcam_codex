import numpy as np
from isetcam.sensor import Sensor, sensor_stats, sensor_photon_noise


def test_sensor_stats_basic():
    volts = np.array([[1.0, 2.0], [3.0, 4.0]])
    s = Sensor(volts=volts.copy(), wave=np.array([550]), exposure_time=0.01)

    mean_signal, noise_sd, snr = sensor_stats(s, (0, 0, 2, 2))

    expected_mean = volts.mean()
    expected_sd = volts.std()
    expected_snr = expected_mean / expected_sd

    assert np.allclose(mean_signal, expected_mean)
    assert np.allclose(noise_sd, expected_sd)
    assert np.allclose(snr, expected_snr)


def test_sensor_stats_with_photon_noise():
    np.random.seed(0)
    volts = np.full((10, 10), 20.0, dtype=float)
    s = Sensor(volts=volts.copy(), wave=np.array([550]), exposure_time=0.01)

    mean_signal, noise_sd, snr = sensor_stats(s, (0, 0, 10, 10), use_photon_noise=True)

    np.random.seed(0)
    s2 = Sensor(volts=volts.copy(), wave=np.array([550]), exposure_time=0.01)
    noisy, noise = sensor_photon_noise(s2)
    exp_mean = noisy.mean()
    exp_sd = noise.std()
    exp_snr = exp_mean / exp_sd

    assert np.allclose(mean_signal, exp_mean)
    assert np.allclose(noise_sd, exp_sd)
    assert np.allclose(snr, exp_snr)
