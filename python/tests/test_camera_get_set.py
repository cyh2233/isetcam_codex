import numpy as np

from isetcam.sensor import Sensor
from isetcam.opticalimage import OpticalImage
from isetcam.camera import Camera, camera_get, camera_set


def test_camera_get_set():
    wave = np.array([500, 510, 520])
    volts = np.ones((2, 2, 3))
    photons = np.ones((2, 2, 3))
    sensor = Sensor(volts=volts.copy(), wave=wave, exposure_time=0.01)
    oi = OpticalImage(photons=photons.copy(), wave=wave)
    cam = Camera(sensor=sensor, optical_image=oi, name="orig")

    assert camera_get(cam, "sensor") is sensor
    assert camera_get(cam, "optical image") is oi
    assert camera_get(cam, "n wave") == 3
    assert camera_get(cam, "name") == "orig"

    new_sensor = Sensor(volts=np.zeros_like(volts), wave=wave, exposure_time=0.02)
    camera_set(cam, "sensor", new_sensor)
    assert camera_get(cam, "sensor") is new_sensor

    new_oi = OpticalImage(photons=np.zeros_like(photons), wave=wave)
    camera_set(cam, "optical_image", new_oi)
    assert camera_get(cam, "oi") is new_oi

    camera_set(cam, "name", "new")
    assert camera_get(cam, "name") == "new"
