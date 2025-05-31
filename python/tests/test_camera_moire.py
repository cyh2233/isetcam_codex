import numpy as np

from isetcam.camera import camera_create, camera_moire


def test_camera_moire_basic():
    cam = camera_create()
    pattern, returned = camera_moire(cam, size=32)
    assert returned is cam
    assert pattern.shape == cam.sensor.volts.shape
    assert np.all(pattern >= 0)
    assert np.all(pattern <= 1)
