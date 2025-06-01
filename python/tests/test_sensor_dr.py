import numpy as np

from isetcam.sensor import Sensor, sensor_set, sensor_dr


def _expected(cg, read_noise, gain_sd, offset_sd, dark_v, v_swing, t):
    dark_volts = dark_v * t
    vmax = v_swing - dark_volts
    dk_e = dark_volts / cg
    dk_var = dk_e * (cg ** 2)
    rn_var = (read_noise * cg) ** 2
    dsnu_var = offset_sd ** 2
    prnu_var = (gain_sd / 100.0 * vmax) ** 2
    vmin = np.sqrt(dk_var + rn_var + dsnu_var + prnu_var)
    if vmin == 0 or vmax <= 0:
        dr = np.inf
    else:
        dr = 10 * np.log10(vmax / vmin)
    return dr, vmax, vmin


def test_sensor_dr_basic():
    s = Sensor(volts=np.zeros((1,)), wave=np.array([550]), exposure_time=0.1)
    sensor_set(s, "conversion_gain", 2.0)
    sensor_set(s, "read_noise_electrons", 1.0)
    sensor_set(s, "gain_sd", 10.0)
    sensor_set(s, "offset_sd", 0.5)
    sensor_set(s, "voltage_swing", 5.0)
    s.dark_voltage = 0.05

    dr, vmax, vmin = sensor_dr(s)
    exp_dr, exp_vmax, exp_vmin = _expected(2.0, 1.0, 10.0, 0.5, 0.05, 5.0, 0.1)

    assert np.isclose(dr, exp_dr)
    assert np.isclose(vmax, exp_vmax)
    assert np.isclose(vmin, exp_vmin)


def test_sensor_dr_infinite():
    s = Sensor(volts=np.zeros((1,)), wave=np.array([550]), exposure_time=0.01)
    sensor_set(s, "conversion_gain", 1.0)
    sensor_set(s, "read_noise_electrons", 0.0)
    sensor_set(s, "gain_sd", 0.0)
    sensor_set(s, "offset_sd", 0.0)
    sensor_set(s, "voltage_swing", 1.0)
    s.dark_voltage = 0.0

    dr, vmax, vmin = sensor_dr(s)
    assert np.isinf(dr)
    assert vmax == 1.0
    assert vmin == 0.0
