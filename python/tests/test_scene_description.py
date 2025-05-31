import numpy as np

from isetcam.scene import Scene, scene_description
from isetcam.luminance_from_photons import luminance_from_photons


def test_scene_description_basic():
    wave = np.array([500, 510, 520])
    photons = np.ones((2, 3, 3))
    sc = Scene(photons=photons.copy(), wave=wave, name="demo")
    desc = scene_description(sc)

    assert "demo" in desc
    assert "2 x 3" in desc
    assert "500:10:520" in desc
    expected_lum = luminance_from_photons(photons, wave).mean()
    assert f"{expected_lum:.4g}" in desc
