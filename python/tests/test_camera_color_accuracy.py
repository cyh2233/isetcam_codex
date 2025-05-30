import numpy as np

from isetcam.camera import camera_create, camera_color_accuracy


def test_camera_color_accuracy_basic():
    cam = camera_create()
    res, returned = camera_color_accuracy(cam, lum=50, patch_size=4)
    assert returned is cam
    assert res["deltaE"].shape == (24,)
    assert np.isclose(res["deltaE"][3], 0.0)
    assert np.all(np.isfinite(res["deltaE"]))
