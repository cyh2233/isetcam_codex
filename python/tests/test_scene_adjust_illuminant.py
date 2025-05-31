import numpy as np
from pathlib import Path

from isetcam.scene import Scene, scene_adjust_illuminant
from isetcam.luminance_from_photons import luminance_from_photons
from isetcam import data_path


def _simple_scene() -> Scene:
    wave = np.array([500, 510, 520])
    photons = np.ones((2, 2, 3))
    return Scene(photons=photons, wave=wave)


def test_scene_adjust_illuminant_vector():
    sc = _simple_scene()
    spd = np.array([1.0, 2.0, 3.0])
    out = scene_adjust_illuminant(sc, spd)
    lum_before = luminance_from_photons(sc.photons, sc.wave).mean()
    lum_after = luminance_from_photons(out.photons, out.wave).mean()
    assert np.isclose(lum_after, lum_before)
    assert not np.allclose(out.photons, sc.photons)


def test_scene_adjust_illuminant_matfile():
    sc = _simple_scene()
    path = data_path("lights/D65.mat")
    out = scene_adjust_illuminant(sc, path)
    lum_before = luminance_from_photons(sc.photons, sc.wave).mean()
    lum_after = luminance_from_photons(out.photons, out.wave).mean()
    assert np.isclose(lum_after, lum_before)
    assert not np.allclose(out.photons, sc.photons)
