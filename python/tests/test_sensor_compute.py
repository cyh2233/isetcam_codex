import numpy as np
from isetcam.sensor import (
    Sensor,
    sensor_compute,
    auto_exposure,
)
from isetcam.opticalimage import OpticalImage


def _simple_oi(width: int = 2, height: int = 2, n_wave: int = 3) -> OpticalImage:
    wave = np.arange(500, 500 + 10 * n_wave, 10)
    photons = np.arange(width * height * n_wave, dtype=float).reshape((height, width, n_wave))
    return OpticalImage(photons=photons, wave=wave)


def test_sensor_compute_no_qe():
    oi = _simple_oi()
    s = Sensor(volts=np.zeros((2, 2)), wave=oi.wave, exposure_time=0.5)
    sensor_compute(s, oi)
    expected = oi.photons.sum(axis=2) * 0.5
    assert np.allclose(s.volts, expected)


def test_sensor_compute_with_qe():
    oi = _simple_oi()
    qe = np.array([0.5, 1.0, 0.0])
    s = Sensor(volts=np.zeros((2, 2)), wave=oi.wave, exposure_time=2.0)
    s.qe = qe
    sensor_compute(s, oi)
    expected = (oi.photons * qe).sum(axis=2) * 2.0
    assert np.allclose(s.volts, expected)


def test_sensor_compute_auto_exposure():
    oi = OpticalImage(photons=10.0 * np.ones((2, 2, 1)), wave=np.array([500]))
    s = Sensor(volts=np.zeros((2, 2)), wave=oi.wave, exposure_time=1.0)
    s.voltage_swing = 5.0
    s.auto_exposure = True
    sensor_compute(s, oi)
    expected_time = 0.95 * 5.0 / 10.0
    assert np.isclose(s.exposure_time, expected_time)
    expected = np.full((2, 2), 10.0 * expected_time)
    assert np.allclose(s.volts, expected)


def test_sensor_compute_color_filters():
    oi = OpticalImage(photons=np.ones((2, 2, 1)), wave=np.array([500]))
    s = Sensor(volts=np.zeros((2, 2)), wave=oi.wave, exposure_time=1.0)
    s.filter_spectra = np.array([[1.0, 0.5]])
    s.filter_names = ["r", "g"]
    s.filter_color_letters = "rggr"
    sensor_compute(s, oi)
    expected = np.array([[1.0, 0.5], [0.5, 1.0]])
    assert np.allclose(s.volts, expected)


def test_sensor_compute_noise_gain_offset():
    np.random.seed(0)
    oi = OpticalImage(photons=np.ones((1, 1, 1)) * 4.0, wave=np.array([500]))
    s = Sensor(volts=np.zeros((1, 1)), wave=oi.wave, exposure_time=1.0)
    s.gain_sd = 10.0
    s.offset_sd = 0.1
    s.analog_gain = 2.0
    s.analog_offset = 1.0
    sensor_compute(s, oi)
    np.random.seed(0)
    g = 1.0 + 0.1 * np.random.randn(1, 1)
    o = 0.1 * np.random.randn(1, 1)
    expected = (4.0 * g + o) * 2.0 + 1.0
    assert np.allclose(s.volts, expected)


def test_auto_exposure_function():
    oi = OpticalImage(photons=5.0 * np.ones((1, 1, 1)), wave=np.array([500]))
    s = Sensor(volts=np.zeros((1, 1)), wave=oi.wave, exposure_time=1.0)
    s.voltage_swing = 4.0
    t = auto_exposure(s, oi)
    expected_t = 0.95 * 4.0 / 5.0
    assert np.isclose(t, expected_t)
