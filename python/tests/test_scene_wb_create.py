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
        wav = sc["wave"]
        wav = wav.ravel()[0] if wav.size == 1 else wav.ravel()[0]
        assert wav == w
        saved = sc["photons"]
        if saved.shape == (1, 1):
            saved = saved[0, 0]
        assert saved.shape == (2, 2, 1)
        idx = np.where(wave == w)[0][0]
        assert np.allclose(saved.squeeze(), photons[:, :, idx])


def test_scene_wb_create_default_scene(tmp_path):
    paths = scene_wb_create(work_dir=tmp_path, patch_size=2, illuminant="D65")
    # D65 data has 107 wavelengths
    assert len(paths) == 107
    sample = loadmat(paths[0])
    sc = sample["scene"]
    photons = sc["photons"]
    if photons.shape == (1, 1):
        photons = photons[0, 0]
    assert photons.shape[0] == 8  # 4 rows * patch_size
    assert photons.shape[1] == 12  # 6 cols * patch_size
