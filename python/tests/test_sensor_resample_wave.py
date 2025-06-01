import numpy as np
from isetcam.sensor import Sensor, sensor_resample_wave


def test_sensor_resample_wave_basic():
    wave = np.array([400, 500, 600, 700], dtype=float)
    volts = np.zeros((2, 2), dtype=float)
    s = Sensor(volts=volts, wave=wave, exposure_time=0.01)
    s.qe = wave * 0.01
    s.filter_spectra = np.vstack((wave, wave ** 2)).T
    s.ir_filter = wave * 0.001

    new_wave = np.array([450, 550, 650], dtype=float)
    out = sensor_resample_wave(s, new_wave)

    assert np.array_equal(out.wave, new_wave)
    assert np.allclose(out.volts, volts)

    expected_qe = np.interp(new_wave, wave, s.qe)
    assert np.allclose(out.qe, expected_qe)

    for i in range(s.filter_spectra.shape[1]):
        expected = np.interp(new_wave, wave, s.filter_spectra[:, i])
        assert np.allclose(out.filter_spectra[:, i], expected)

    expected_ir = np.interp(new_wave, wave, s.ir_filter)
    assert np.allclose(out.ir_filter, expected_ir)
