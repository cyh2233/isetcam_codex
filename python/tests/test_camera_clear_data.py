import numpy as np

from isetcam.camera import Camera, camera_clear_data
from isetcam.sensor import Sensor
from isetcam.opticalimage import OpticalImage
from isetcam.ip import VCImage


def _simple_camera() -> Camera:
    sensor = Sensor(volts=np.ones((2, 2)), exposure_time=0.01, wave=np.array([500, 510]))
    oi = OpticalImage(photons=np.ones((2, 2, 2)), wave=np.array([500, 510]))
    cam = Camera(sensor=sensor, optical_image=oi)
    cam.ip = VCImage(rgb=np.ones((2, 2, 3)), wave=np.array([500, 510]))
    return cam


def test_camera_clear_data_removes_nested_fields():
    cam = _simple_camera()
    cam.sensor.offset_fpn_image = np.ones((2, 2))
    cam.optical_image.depth_map = np.ones((2, 2))
    cam.ip.processed_rgb = np.zeros((2, 2, 3))
    cam.ip.custom_attr = 42

    out = camera_clear_data(cam)
    assert out is cam
    assert not hasattr(cam.sensor, "offset_fpn_image")
    assert not hasattr(cam.optical_image, "depth_map")
    assert not hasattr(cam.ip, "processed_rgb")
    assert not hasattr(cam.ip, "custom_attr")


def test_camera_clear_data_no_fields():
    cam = _simple_camera()
    out = camera_clear_data(cam)
    assert out is cam
    assert np.allclose(cam.sensor.volts, np.ones((2, 2)))
    assert np.allclose(cam.optical_image.photons, np.ones((2, 2, 2)))
    assert np.allclose(cam.ip.rgb, np.ones((2, 2, 3)))
