import numpy as np

from isetcam.sensor import Sensor
from isetcam.display import Display, display_apply_gamma
from isetcam.ip import ip_compute, ip_create, ip_set, ip_get, ip_demosaic


def _simple_sensor() -> Sensor:
    volts = np.array([[0.2, 0.4], [0.6, 0.8]], dtype=float)
    wave = np.array([500, 510])
    return Sensor(volts=volts, exposure_time=0.01, wave=wave)


def _simple_display(n_levels: int = 4) -> Display:
    wave = np.array([500, 510])
    spd = np.ones((2, 3))
    gamma_vals = np.linspace(0, 1, n_levels) ** 2
    gamma = gamma_vals.reshape(n_levels, 1).repeat(3, axis=1)
    return Display(spd=spd, wave=wave, gamma=gamma)


def test_ip_compute_pipeline():
    sensor = _simple_sensor()
    disp = _simple_display()
    ip = ip_compute(sensor, disp)
    expected_lin = ip_demosaic(sensor.volts, "rggb", method="bilinear")
    expected = display_apply_gamma(expected_lin, disp, inverse=True)
    assert np.allclose(ip.rgb, expected)


def test_ip_set_new_params():
    sensor = _simple_sensor()
    disp = _simple_display()
    ip = ip_create(sensor, disp)
    ip_set(ip, "demosaic method", "nearest")
    ip_set(ip, "internal cs", "linear sRGB")
    ip_set(ip, "conversion method sensor", "current")
    ip_set(ip, "illuminant correction method", "gray world")
    assert ip_get(ip, "demosaic method") == "nearest"
    assert ip_get(ip, "internal cs") == "linear sRGB"
    assert ip_get(ip, "conversion method sensor") == "current"
    assert ip_get(ip, "illuminant correction method") == "gray world"
