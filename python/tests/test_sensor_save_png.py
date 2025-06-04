import numpy as np
import imageio.v2 as imageio

from isetcam.sensor import Sensor, sensor_save_png


def test_sensor_save_png(tmp_path):
    volts = np.ones((1, 1, 3), dtype=float) * 0.5
    sensor = Sensor(volts=volts, exposure_time=0.01, wave=np.array([500, 600, 700]))
    path = tmp_path / "s.png"
    sensor_save_png(sensor, path)
    img = imageio.imread(path)
    assert img.shape == (1, 1, 3)
