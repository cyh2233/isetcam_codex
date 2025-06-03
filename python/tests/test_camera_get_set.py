import numpy as np

from isetcam.sensor import Sensor
from isetcam.opticalimage import OpticalImage
from isetcam.camera import Camera, camera_get, camera_set
from isetcam.optics import Optics
from isetcam.ip import VCImage


def test_camera_get_set():
    wave = np.array([500, 510, 520])
    volts = np.ones((2, 2, 3))
    photons = np.ones((2, 2, 3))
    sensor = Sensor(volts=volts.copy(), wave=wave, exposure_time=0.01)
    oi = OpticalImage(photons=photons.copy(), wave=wave)
    cam = Camera(sensor=sensor, optical_image=oi, name="orig")

    assert camera_get(cam, "Sensor") is sensor
    assert camera_get(cam, "OPTICAL IMAGE") is oi
    assert camera_get(cam, "N WAVE") == 3
    assert camera_get(cam, " NAME ") == "orig"

    new_sensor = Sensor(volts=np.zeros_like(volts), wave=wave, exposure_time=0.02)
    camera_set(cam, " SENSOR ", new_sensor)
    assert camera_get(cam, " SENSOR") is new_sensor

    new_oi = OpticalImage(photons=np.zeros_like(photons), wave=wave)
    camera_set(cam, " OPTICAL_image", new_oi)
    assert camera_get(cam, "oi") is new_oi

    camera_set(cam, " NaMe", "new")
    assert camera_get(cam, " NaMe ") == "new"

    # optics and ip forwarding
    cam.optics = Optics(f_number=4.0, f_length=0.005, wave=wave)
    cam.ip = VCImage(rgb=np.zeros_like(volts), wave=wave,
                     illuminant_correction_method="gray world")

    assert camera_get(cam, "optics fnumber") == 4.0
    camera_set(cam, "optics fnumber", 2.8)
    assert camera_get(cam, "optics f_number") == 2.8

    assert camera_get(cam, "ip illuminant correction method") == "gray world"
    camera_set(cam, "ip illuminant correction method", "none")
    assert camera_get(cam, "ip illuminant correction method") == "none"
