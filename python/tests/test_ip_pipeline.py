import numpy as np

from isetcam.sensor import Sensor
from isetcam.display import Display
from isetcam.ip import VCImage, ip_create, ip_compute


def _simple_sensor() -> Sensor:
    wave = np.array([500, 510])
    volts = np.full((2, 2), 0.5)
    return Sensor(volts=volts, wave=wave, exposure_time=1.0)


def _simple_display(n_levels: int = 4) -> Display:
    wave = np.array([500, 510])
    spd = np.ones((2, 3))
    gamma = np.linspace(0, 1, n_levels).reshape(n_levels, 1).repeat(3, axis=1)
    return Display(spd=spd, wave=wave, gamma=gamma)


def test_ip_create():
    sensor = _simple_sensor()
    disp = _simple_display()
    ip = ip_create(sensor, disp)
    assert isinstance(ip, VCImage)
    assert ip.rgb.shape == (2, 2, 3)
    assert np.array_equal(ip.wave, sensor.wave)


def test_ip_compute():
    sensor = _simple_sensor()
    disp = _simple_display()
    ip = ip_compute(sensor, disp)
    expected = np.full((2, 2, 3), 0.5)
    assert np.allclose(ip.rgb, expected)
