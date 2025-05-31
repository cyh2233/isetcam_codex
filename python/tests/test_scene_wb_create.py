import numpy as np
from scipy.io import loadmat

from isetcam.scene import scene_wb_create, Scene


def test_scene_wb_create_basic(tmp_path):
    wave = np.array([500, 510])
    photons = np.arange(8).reshape(2, 2, 2).astype(float)
    scene = Scene(photons=photons, wave=wave, name="test")
    paths = scene_wb_create(scene, tmp_path)
    assert len(paths) == 2
    for p, w in zip(paths, wave):
        assert p.exists()
        data = loadmat(p)
        sc = data["scene"]
        assert sc["wave"].ravel()[0] == w
        saved = sc["photons"]
        assert saved.shape == (2, 2, 1)
        assert np.allclose(saved.squeeze(), photons[:, :, np.where(wave == w)[0][0]])


def test_scene_wb_create_default_scene(tmp_path):
    paths = scene_wb_create(work_dir=tmp_path, patch_size=2, illuminant="D65")
    # D65 data has 107 wavelengths
    assert len(paths) == 107
    sample = loadmat(paths[0])
    sc = sample["scene"]
    assert sc["photons"].shape[0] == 8  # 4 rows * patch_size
    assert sc["photons"].shape[1] == 12  # 6 cols * patch_size
