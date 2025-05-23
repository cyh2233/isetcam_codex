import numpy as np
from isetcam.scene import Scene, scene_add


def _simple_scene(scale: float) -> Scene:
    wave = np.array([500, 510])
    photons = np.ones((2, 2, 2)) * scale
    return Scene(photons=photons, wave=wave)


def test_scene_add_pair_add():
    s1 = _simple_scene(1.0)
    s2 = _simple_scene(2.0)
    out = scene_add(s1, s2, "add")
    assert np.allclose(out.photons, s1.photons + s2.photons)


def test_scene_add_pair_average():
    s1 = _simple_scene(1.0)
    s2 = _simple_scene(3.0)
    out = scene_add(s1, s2, "average")
    expected = (s1.photons + s2.photons) / 2
    assert np.allclose(out.photons, expected)


def test_scene_add_pair_remove_spatial_mean():
    wave = np.array([500, 510])
    base = np.zeros((2, 2, 2))
    pattern = np.stack(
        [np.array([[1, 2], [3, 4]]), np.array([[5, 6], [7, 8]])], axis=2
    )
    s1 = Scene(photons=base, wave=wave)
    s2 = Scene(photons=pattern, wave=wave)
    out = scene_add(s1, s2, "remove spatial mean")
    expected = pattern - pattern.mean(axis=(0, 1), keepdims=True)
    assert np.allclose(out.photons, expected)


def test_scene_add_weighted_list():
    s1 = _simple_scene(1.0)
    s2 = _simple_scene(2.0)
    out = scene_add([s1, s2], [0.5, 0.25], "add")
    expected = 0.5 * s1.photons + 0.25 * s2.photons
    assert np.allclose(out.photons, expected)
