import numpy as np
from isetcam.sensor import Sensor, sensor_wb_compute
from isetcam.opticalimage import OpticalImage


def test_sensor_wb_compute_basic_sum():
    wave = np.array([500, 510, 520])
    s = Sensor(volts=np.zeros((2, 2)), wave=wave, exposure_time=0.5)
    oi1 = OpticalImage(photons=np.ones((2, 2)), wave=np.array([500]), name="500")
    oi2 = OpticalImage(photons=2 * np.ones((2, 2)), wave=np.array([510]), name="510")
    oi3 = OpticalImage(photons=3 * np.ones((2, 2)), wave=np.array([520]), name="520")

    sensor_wb_compute(s, [oi1, oi2, oi3])

    expected = (1 + 2 + 3) * 0.5 * np.ones((2, 2))
    assert np.allclose(s.volts, expected)
    assert s.name == "wb-520"


def test_sensor_wb_compute_with_qe():
    wave = np.array([500, 510])
    s = Sensor(volts=np.zeros((1, 1)), wave=wave, exposure_time=1.0)
    s.qe = np.array([1.0, 2.0])
    oi1 = OpticalImage(photons=np.ones((1, 1)), wave=np.array([500]))
    oi2 = OpticalImage(photons=np.ones((1, 1)), wave=np.array([510]))

    sensor_wb_compute(s, [oi1, oi2])

    expected = 1.0 * 1.0 + 1.0 * 2.0
    assert np.allclose(s.volts, expected)
