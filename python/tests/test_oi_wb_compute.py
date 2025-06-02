import numpy as np
from scipy.io import loadmat

from isetcam.scene import Scene, scene_wb_create
from isetcam.opticalimage import oi_wb_compute
from isetcam.optics import Optics


def _simple_scene() -> Scene:
    wave = np.array([500, 510], dtype=float)
    photons = np.arange(8, dtype=float).reshape((2, 2, 2))
    return Scene(photons=photons, wave=wave, name="test")


def test_oi_wb_compute_basic(tmp_path):
    scene = _simple_scene()
    scene_wb_create(scene, tmp_path)
    optics = Optics(f_number=2.0, f_length=1.0, wave=np.array([500], dtype=float))
    paths = oi_wb_compute(tmp_path, optics)
    assert len(paths) == 2
    for path, w in zip(paths, scene.wave):
        assert path.exists()
        data = loadmat(path)
        oi = data["oi"]
        saved = oi["photons"]
        if saved.shape == (1, 1):
            saved = saved[0, 0]
        assert saved.shape == (2, 2, 1)
        idx = np.where(scene.wave == w)[0][0]
        scale = (optics.f_length / optics.f_number) ** 2
        expected = scene.photons[:, :, idx:idx + 1] * scale
        assert np.allclose(saved, expected)
        wav = oi["wave"].ravel()[0]
        assert wav == w


def test_oi_wb_compute_default_optics(tmp_path):
    scene = _simple_scene()
    scene_wb_create(scene, tmp_path)
    paths = oi_wb_compute(tmp_path)
    assert len(paths) == 2
    for path, w in zip(paths, scene.wave):
        data = loadmat(path)
        oi = data["oi"]
        wav = oi["wave"].ravel()[0]
        assert wav == w
