import numpy as np
from isetcam.sensor import Sensor, sensor_compute
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
