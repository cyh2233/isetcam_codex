import numpy as np
import pytest
import matplotlib

matplotlib.use("Agg")

from isetcam.sensor import Sensor, sensor_show_image
from isetcam.display import Display


def _matplotlib_available() -> bool:
    try:
        import matplotlib.pyplot as _  # noqa: F401
        return True
    except Exception:
        return False


@pytest.mark.skipif(not _matplotlib_available(), reason="matplotlib not installed")
def test_sensor_show_image_runs():
    volts = np.array([[[0.2, 0.4, 0.6]]], dtype=float)
    wave = np.array([500, 600, 700])
    sensor = Sensor(volts=volts, wave=wave, exposure_time=0.01)
    disp = Display(spd=np.eye(3), wave=wave, gamma=None)
    ax = sensor_show_image(sensor, disp)
    assert ax is not None


@pytest.mark.skipif(not _matplotlib_available(), reason="matplotlib not installed")
def test_sensor_show_image_wave_mismatch():
    volts = np.array([[[0.2, 0.4, 0.6]]], dtype=float)
    wave = np.array([500, 600, 700])
    sensor = Sensor(volts=volts, wave=wave, exposure_time=0.01)
    disp = Display(spd=np.eye(3), wave=np.array([400, 500, 600, 700]), gamma=None)
    with pytest.raises(ValueError, match="display.spd must be resampled"):
        sensor_show_image(sensor, disp)
