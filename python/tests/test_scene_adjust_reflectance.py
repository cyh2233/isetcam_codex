import numpy as np

from isetcam.scene import Scene, scene_adjust_reflectance


def _simple_scene() -> Scene:
    wave = np.array([500, 510, 520])
    illum = np.array([1.0, 2.0, 3.0])
    refl = np.full(3, 0.5)
    photons = np.tile(refl.reshape(1, 1, -1), (2, 2, 1)) * illum.reshape(1, 1, -1)
    sc = Scene(photons=photons, wave=wave)
    sc.illuminant = illum
    sc.reflectance = refl
    return sc


def test_scene_adjust_reflectance_vector():
    sc = _simple_scene()
    new_r = np.array([0.2, 0.4, 0.6])
    out = scene_adjust_reflectance(sc, new_r)
    expected = np.tile(new_r.reshape(1, 1, -1), (2, 2, 1)) * sc.illuminant.reshape(1, 1, -1)
    assert np.allclose(out.photons, expected)
    assert np.allclose(out.reflectance, new_r)


def test_scene_adjust_reflectance_cube():
    sc = _simple_scene()
    new_r = np.array(
        [
            [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]],
            [[0.7, 0.8, 0.9], [0.2, 0.4, 0.6]],
        ]
    )
    out = scene_adjust_reflectance(sc, new_r)
    expected = new_r * sc.illuminant.reshape(1, 1, -1)
    assert np.allclose(out.photons, expected)
    assert np.allclose(out.reflectance, new_r)
