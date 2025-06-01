import numpy as np
from isetcam.scene import Scene
from isetcam.human import human_oi


def test_human_oi_basic():
    wave = np.array([550], dtype=float)
    photons = np.ones((8, 8, 1), dtype=float)
    sc = Scene(photons=photons, wave=wave)
    sc.sample_spacing = 1e-3
    oi = human_oi(sc)
    assert oi.photons.shape == photons.shape
    assert hasattr(oi, "illuminance")
    assert oi.illuminance.shape == photons.shape[:2]
