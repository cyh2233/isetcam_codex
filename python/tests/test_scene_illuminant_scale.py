import numpy as np

from isetcam.scene import Scene, scene_illuminant_scale
from isetcam.luminance_from_photons import luminance_from_photons


def _simple_scene() -> Scene:
    wave = np.array([500, 510], dtype=float)
    photons = np.array(
        [[[0.2, 0.4], [0.6, 0.8]], [[0.5, 0.2], [0.3, 0.4]]], dtype=float
    )
    sc = Scene(photons=photons, wave=wave)
    sc.illuminant = np.array([1.0, 1.0])
    return sc


def test_scene_illuminant_scale_vector():
    sc = _simple_scene()
    out = scene_illuminant_scale(sc)
    refl = out.photons / out.illuminant.reshape(1, 1, -1)
    assert np.isclose(refl.mean(), 1.0)
    assert np.allclose(out.photons, sc.photons)
    lum_before = luminance_from_photons(sc.photons, sc.wave).mean()
    lum_after = luminance_from_photons(out.photons, out.wave).mean()
    assert np.isclose(lum_after, lum_before)


def test_scene_illuminant_scale_cube():
    sc = _simple_scene()
    sc.illuminant = np.ones_like(sc.photons)
    sc.illuminant[0, 0, :] = 2.0
    out = scene_illuminant_scale(sc)
    refl = out.photons / out.illuminant
    assert np.isclose(refl.mean(), 1.0)

