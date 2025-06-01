import numpy as np

from isetcam.sensor import Sensor, sensor_set, sensor_iso_speed


def _expected_iso(cg, read_noise, gain_sd, offset_sd, vpls):
    gain_sd = gain_sd / 100.0
    dsnu = offset_sd / cg
    a = 100.0 * gain_sd ** 2 - 1.0
    b = 100.0
    c = 100.0 * (read_noise ** 2 + dsnu ** 2)
    if a >= 0:
        return float("inf")
    disc = b ** 2 - 4.0 * a * c
    e1 = (-b + np.sqrt(disc)) / (2.0 * a)
    e2 = (-b - np.sqrt(disc)) / (2.0 * a)
    e = e1 if e1 > 0 else e2
    luxsec = e / (cg * vpls)
    return 10.0 / luxsec


def test_iso_speed_shot_noise_only():
    s = Sensor(volts=np.zeros((1,)), wave=np.array([550]), exposure_time=0.01)
    sensor_set(s, "conversion_gain", 1.0)
    sensor_set(s, "read_noise_electrons", 0.0)
    sensor_set(s, "gain_sd", 0.0)
    sensor_set(s, "offset_sd", 0.0)
    s.volts_per_lux_sec = 1000.0

    iso = sensor_iso_speed(s)
    exp_iso = _expected_iso(1.0, 0.0, 0.0, 0.0, 1000.0)
    assert np.isclose(iso, exp_iso)


def test_iso_speed_with_read_noise():
    s = Sensor(volts=np.zeros((1,)), wave=np.array([550]), exposure_time=0.01)
    sensor_set(s, "conversion_gain", 1.0)
    sensor_set(s, "read_noise_electrons", 20.0)
    sensor_set(s, "gain_sd", 0.0)
    sensor_set(s, "offset_sd", 0.0)
    s.volts_per_lux_sec = 1000.0

    iso = sensor_iso_speed(s)
    exp_iso = _expected_iso(1.0, 20.0, 0.0, 0.0, 1000.0)
    assert np.isclose(iso, exp_iso)
