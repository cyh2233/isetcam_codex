import numpy as np

from isetcam.camera import camera_create, Camera
from isetcam.sensor import sensor_create, Sensor
from isetcam.optics import optics_create, Optics
from isetcam.opticalimage import OpticalImage


def test_camera_create_default():
    cam = camera_create()
    assert isinstance(cam, Camera)
    assert isinstance(cam.sensor, Sensor)
    assert isinstance(cam.optical_image, OpticalImage)
    assert hasattr(cam, "optics")
    assert isinstance(cam.optics, Optics)
    assert np.array_equal(cam.sensor.wave, cam.optical_image.wave)


def test_camera_create_custom():
    wave = np.array([500, 510])
    s = sensor_create(wave=wave)
    o = optics_create(wave=wave)
    cam = camera_create(sensor=s, optics=o, name="demo")
    assert cam.name == "demo"
    assert cam.sensor is s
    assert cam.optics is o
    assert np.array_equal(cam.optical_image.wave, wave)
