import numpy as np
import pytest
import matplotlib

matplotlib.use("Agg")

from isetcam.camera import Camera, camera_show
from isetcam.sensor import Sensor
from isetcam.opticalimage import OpticalImage
from isetcam.ip import VCImage
from isetcam.display import Display, display_create
import importlib


def _matplotlib_available() -> bool:
    try:
        import matplotlib.pyplot as _  # noqa: F401
        return True
    except Exception:
        return False


def _simple_camera() -> Camera:
    wave = np.array([500, 600, 700])
    sensor = Sensor(volts=np.ones((1, 1, 3)), exposure_time=0.01, wave=wave)
    oi = OpticalImage(photons=np.ones((1, 1, 3)), wave=wave)
    cam = Camera(sensor=sensor, optical_image=oi)
    cam.ip = VCImage(rgb=np.ones((1, 1, 3)), wave=wave)
    return cam


@pytest.mark.skipif(not _matplotlib_available(), reason="matplotlib not installed")
def test_camera_show_oi_sensor_ip(monkeypatch):
    cam = _simple_camera()
    disp = Display(spd=np.eye(3), wave=cam.sensor.wave, gamma=None)
    oi_mod = importlib.import_module("isetcam.opticalimage.oi_show_image")
    sensor_mod = importlib.import_module("isetcam.sensor.sensor_show_image")
    monkeypatch.setattr(oi_mod, "display_create", lambda: disp)
    monkeypatch.setattr(sensor_mod, "display_create", lambda: disp)

    ax1 = camera_show(cam, which="oi")
    assert ax1 is not None
    ax2 = camera_show(cam, which="sensor")
    assert ax2 is not None
    ax3 = camera_show(cam, which="ip")
    assert ax3 is not None
