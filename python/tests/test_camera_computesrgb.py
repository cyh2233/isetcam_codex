import numpy as np

from isetcam.camera import camera_create, camera_computesrgb


def test_camera_computesrgb_basic():
    cam = camera_create()
    srgb_res, srgb_ideal, volts = camera_computesrgb(
        cam,
        scene="macbeth d65",
        patch_size=4,
        mean_luminance=20,
        fov=15,
    )
    assert srgb_res.shape == srgb_ideal.shape
    assert srgb_res.shape[2] == 3
    assert volts.shape == cam.sensor.volts.shape
    assert np.all((srgb_res >= 0) & (srgb_res <= 1))
    assert np.all((srgb_ideal >= 0) & (srgb_ideal <= 1))
    assert np.all(np.isfinite(volts))
