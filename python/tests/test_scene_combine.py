import numpy as np
import pytest

from isetcam.scene import Scene, scene_combine


def _scene(width: int, height: int, value: float) -> Scene:
    wave = np.array([500, 510])
    photons = np.full((height, width, wave.size), value, dtype=float)
    return Scene(photons=photons, wave=wave)


def test_scene_combine_horizontal():
    s1 = _scene(2, 2, 1.0)
    s2 = _scene(3, 2, 2.0)
    out = scene_combine(s1, s2, "horizontal")
    assert out.photons.shape == (2, 5, 2)
    assert np.all(out.photons[:, :2, :] == 1.0)
    assert np.all(out.photons[:, 2:, :] == 2.0)


def test_scene_combine_vertical():
    s1 = _scene(2, 2, 1.0)
    s2 = _scene(2, 1, 2.0)
    out = scene_combine(s1, s2, "vertical")
    assert out.photons.shape == (3, 2, 2)
    assert np.all(out.photons[:2, :, :] == 1.0)
    assert np.all(out.photons[2:, :, :] == 2.0)


def test_scene_combine_both():
    s1 = _scene(1, 1, 1.0)
    s2 = _scene(1, 1, 2.0)
    out = scene_combine(s1, s2, "both")
    expected = np.array(
        [[[1.0, 1.0], [2.0, 2.0]], [[1.0, 1.0], [2.0, 2.0]]]
    )
    assert np.array_equal(out.photons, expected)


def test_scene_combine_centered():
    s1 = _scene(1, 1, 1.0)
    s2 = _scene(1, 1, 2.0)
    out = scene_combine(s1, s2, "centered")
    expected = np.array(
        [
            [[2.0, 2.0], [2.0, 2.0], [2.0, 2.0]],
            [[2.0, 2.0], [1.0, 1.0], [2.0, 2.0]],
            [[2.0, 2.0], [2.0, 2.0], [2.0, 2.0]],
        ]
    )
    assert np.array_equal(out.photons, expected)


def test_scene_combine_wave_mismatch():
    s1 = _scene(1, 1, 1.0)
    s2 = Scene(photons=s1.photons, wave=np.array([500, 520]))
    with pytest.raises(ValueError):
        scene_combine(s1, s2, "horizontal")


def test_scene_combine_size_mismatch():
    s1 = _scene(2, 2, 1.0)
    s2 = _scene(3, 3, 2.0)
    with pytest.raises(ValueError):
        scene_combine(s1, s2, "horizontal")

