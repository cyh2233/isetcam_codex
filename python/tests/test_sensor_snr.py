import numpy as np

from isetcam.sensor import Sensor, sensor_set, sensor_snr, sensor_snr_luxsec


def _expected(volts, cg, read_sd, gain_sd_percent, offset_sd):
    gain_sd = gain_sd_percent / 100.0
    shot_sd = np.sqrt(volts / cg)
    prnu_sd = gain_sd * (volts / cg)
    dsnu_sd = offset_sd / cg
    signal_power = (volts / cg) ** 2
    noise_power = shot_sd ** 2 + read_sd ** 2 + dsnu_sd ** 2 + prnu_sd ** 2
    snr = 10 * np.log10(signal_power / noise_power)
    snr_shot = 10 * np.log10(signal_power / (shot_sd ** 2))
    snr_read = np.inf if read_sd == 0 else 10 * np.log10(signal_power / (read_sd ** 2))
    snr_dsnu = np.inf if dsnu_sd == 0 else 10 * np.log10(signal_power / (dsnu_sd ** 2))
    snr_prnu = np.inf if np.all(prnu_sd == 0) else 10 * np.log10(signal_power / (prnu_sd ** 2))
    return snr, snr_shot, snr_read, snr_dsnu, snr_prnu


def test_sensor_snr_basic():
    s = Sensor(volts=np.zeros((1,)), wave=np.array([550]), exposure_time=0.01)
    sensor_set(s, "conversion_gain", 2.0)
    sensor_set(s, "read_noise_electrons", 1.0)
    sensor_set(s, "gain_sd", 10.0)
    sensor_set(s, "offset_sd", 0.5)
    sensor_set(s, "voltage_swing", 1.0)

    volts = np.array([0.1, 0.5])
    snr, v, snr_shot, snr_read, snr_dsnu, snr_prnu = sensor_snr(s, volts)

    exp_snr, exp_shot, exp_read, exp_dsnu, exp_prnu = _expected(
        volts, 2.0, 1.0, 10.0, 0.5
    )

    assert np.allclose(v, volts)
    assert np.allclose(snr, exp_snr)
    assert np.allclose(snr_shot, exp_shot)
    assert np.allclose(snr_read, exp_read)
    assert np.allclose(snr_dsnu, exp_dsnu)
    assert np.allclose(snr_prnu, exp_prnu)


def test_sensor_snr_luxsec():
    volts = np.zeros((1, 1, 2))
    s = Sensor(volts=volts, wave=np.array([550]), exposure_time=0.01)
    s.volts_per_lux_sec = [1.0, 2.0]

    snr, luxsec = sensor_snr_luxsec(s)
    snr_expected, volts = sensor_snr(s)[:2]

    lux_expected = np.column_stack((volts, volts / 2.0))

    assert np.allclose(snr, snr_expected)
    assert np.allclose(luxsec, lux_expected)
