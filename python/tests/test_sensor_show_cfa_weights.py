import numpy as np

from isetcam.sensor import Sensor, sensor_show_cfa_weights


def test_sensor_show_cfa_weights_runs():
    wgts = np.arange(9, dtype=float).reshape(3, 3)
    s = Sensor(volts=np.zeros((2, 2)), wave=np.array([500]), exposure_time=0.01)
    s.filter_color_letters = "rggb"
    img = sensor_show_cfa_weights(wgts, s)
    assert img.shape == (3 * 32, 3 * 32, 3)
    assert img.min() >= 0.0 and img.max() <= 1.0


def test_sensor_show_cfa_weights_constant():
    wgts = np.ones((3, 3), dtype=float)
    s = Sensor(volts=np.zeros((2, 2)), wave=np.array([500]), exposure_time=0.01)
    s.filter_color_letters = "rggb"
    img = sensor_show_cfa_weights(wgts, s, img_scale=1)
    assert img.shape == (3, 3, 3)
    assert img.min() >= 0.0 and img.max() <= 1.0
