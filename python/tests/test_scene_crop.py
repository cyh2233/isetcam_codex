import numpy as np
import pytest

from isetcam.scene import Scene, scene_crop


def _simple_scene(width: int = 4, height: int = 4, n_wave: int = 2) -> Scene:
    wave = np.arange(400, 400 + 10 * n_wave, 10)
    photons = np.arange(width * height * n_wave, dtype=float).reshape(
        (height, width, n_wave)
    )
    return Scene(photons=photons, wave=wave)


def test_scene_crop_basic():
    sc = _simple_scene(4, 4, 2)
    out = scene_crop(sc, (1, 1, 2, 2))
    expected = sc.photons[1:3, 1:3, :]
    assert np.array_equal(out.photons, expected)
    assert np.array_equal(out.wave, sc.wave)
    assert out.crop_rect == (1, 1, 2, 2)
    assert out.full_size == (4, 4)


def test_scene_crop_out_of_bounds():
    sc = _simple_scene(4, 4, 1)
    with pytest.raises(ValueError):
        scene_crop(sc, (3, 3, 2, 2))
