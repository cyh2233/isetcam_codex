import numpy as np
import pytest

from isetcam.camera import (
    camera_create,
    camera_color_accuracy,
    camera_mtf,
    camera_moire,
    camera_vsnr_sl,
    camera_full_reference,
)
from isetcam.camera.camera_vsnr_sl import VSNRSLResult
from isetcam.scene import Scene
from isetcam.metrics import metrics_camera


def _gray_scene(w: int = 4, h: int = 4, n_wave: int = 3) -> Scene:
    wave = np.arange(500, 500 + 10 * n_wave, 10)
    photons = np.ones((h, w, n_wave), dtype=float)
    return Scene(photons=photons, wave=wave)


def test_metrics_camera_mcccolor():
    cam1 = camera_create()
    cam2 = camera_create()
    metric = metrics_camera(cam1, "mcccolor", lum=20, patch_size=4)
    expected = camera_color_accuracy(cam2, lum=20, patch_size=4)
    assert np.allclose(metric[0]["deltaE"], expected[0]["deltaE"])
    assert metric[1] is cam1


def test_metrics_camera_slantededge():
    cam1 = camera_create()
    cam2 = camera_create()
    freqs, mtf = metrics_camera(cam1, "slantededge")
    efreqs, emtf = camera_mtf(cam2)
    assert np.allclose(freqs, efreqs)
    assert np.allclose(mtf, emtf)


def test_metrics_camera_moire():
    cam1 = camera_create()
    cam2 = camera_create()
    pattern, returned = metrics_camera(cam1, "moire", size=16)
    expected_pattern, _ = camera_moire(cam2, size=16)
    assert returned is cam1
    assert np.allclose(pattern, expected_pattern)


def test_metrics_camera_vsnr():
    cam1 = camera_create()
    cam2 = camera_create()
    levels = [1.0, 2.0]
    res = metrics_camera(cam1, "vsnr", mean_luminances=levels)
    expected = camera_vsnr_sl(cam2, levels)
    assert isinstance(res, VSNRSLResult)
    assert np.allclose(res.vsnr, expected.vsnr)


def test_metrics_camera_fullreference():
    cam1 = camera_create()
    cam2 = camera_create()
    sc = _gray_scene()
    res = metrics_camera(cam1, "fullreference", scene=sc)
    expected = camera_full_reference(cam2, sc)
    assert np.allclose(res["deltaE"], expected["deltaE"])


def test_metrics_camera_unknown():
    cam = camera_create()
    with pytest.raises(ValueError):
        metrics_camera(cam, "unknown")
