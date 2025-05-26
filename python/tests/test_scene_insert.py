import numpy as np
from isetcam.scene import Scene, scene_insert


def _base_scene(width: int = 4, height: int = 4, n_wave: int = 1) -> Scene:
    wave = np.arange(400, 400 + 10 * n_wave, 10)
    photons = np.zeros((height, width, n_wave), dtype=float)
    return Scene(photons=photons, wave=wave)


def _insert_scene(width: int = 2, height: int = 2, n_wave: int = 1) -> Scene:
    wave = np.arange(400, 400 + 10 * n_wave, 10)
    photons = np.arange(width * height * n_wave, dtype=float).reshape(
        (height, width, n_wave)
    )
    return Scene(photons=photons, wave=wave)


def test_scene_insert_in_bounds():
    base = _base_scene(4, 4, 1)
    ins = _insert_scene(2, 2, 1)
    out = scene_insert(base, ins, (1, 1))
    expected = base.photons.copy()
    expected[1:3, 1:3, :] = ins.photons
    assert np.array_equal(out.photons, expected)
    assert np.array_equal(out.wave, base.wave)


def test_scene_insert_partial_out_of_bounds():
    base = _base_scene(4, 4, 1)
    ins = _insert_scene(3, 3, 1)
    out = scene_insert(base, ins, (3, 2))
    expected = base.photons.copy()
    expected[2:4, 3:4, :] = ins.photons[0:2, 0:1, :]
    assert np.array_equal(out.photons, expected)

