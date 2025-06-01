import numpy as np

from isetcam.camera import camera_create, camera_full_reference
from isetcam.scene import Scene


def _gray_scene(w: int = 4, h: int = 4, n_wave: int = 3) -> Scene:
    wave = np.arange(500, 500 + 10 * n_wave, 10)
    photons = np.ones((h, w, n_wave), dtype=float)
    return Scene(photons=photons, wave=wave)


def test_camera_full_reference_basic():
    cam = camera_create()
    sc = _gray_scene()
    res = camera_full_reference(cam, sc)
    assert set(res.keys()) == {"mtf", "deltaE", "vsnr"}

    freqs, mtf = res["mtf"]
    assert freqs.shape == mtf.shape
    assert res["deltaE"].shape == (sc.photons.shape[0], sc.photons.shape[1])
    assert np.isfinite(res["vsnr"])
