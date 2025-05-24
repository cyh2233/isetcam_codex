import numpy as np

from isetcam.scene import Scene, scene_pad, scene_translate


def _simple_scene(width: int = 3, height: int = 3, n_wave: int = 1) -> Scene:
    wave = np.arange(400, 400 + 10 * n_wave, 10)
    photons = np.arange(width * height * n_wave, dtype=float).reshape(
        (height, width, n_wave)
    )
    return Scene(photons=photons, wave=wave)


def test_scene_pad_scalar():
    sc = _simple_scene(2, 2, 1)
    out = scene_pad(sc, 1, value=-1)
    expected = np.pad(sc.photons, ((1, 1), (1, 1), (0, 0)), constant_values=-1)
    assert np.array_equal(out.photons, expected)
    assert np.array_equal(out.wave, sc.wave)


def test_scene_pad_tuple():
    sc = _simple_scene(2, 2, 1)
    out = scene_pad(sc, (1, 2, 3, 4), value=5)
    expected = np.pad(
        sc.photons,
        ((1, 2), (3, 4), (0, 0)),
        constant_values=5,
    )
    assert np.array_equal(out.photons, expected)


def test_scene_translate_positive():
    sc = _simple_scene(3, 3, 1)
    out = scene_translate(sc, 1, 1, fill=-1)
    expected = np.full_like(sc.photons, -1)
    expected[1:, 1:, :] = sc.photons[:-1, :-1, :]
    assert np.array_equal(out.photons, expected)


def test_scene_translate_negative():
    sc = _simple_scene(3, 3, 1)
    out = scene_translate(sc, -1, -1, fill=0)
    expected = np.zeros_like(sc.photons)
    expected[:-1, :-1, :] = sc.photons[1:, 1:, :]
    assert np.array_equal(out.photons, expected)


def test_scene_translate_outside():
    sc = _simple_scene(2, 2, 1)
    out = scene_translate(sc, 5, 0, fill=2)
    expected = np.full_like(sc.photons, 2)
    assert np.array_equal(out.photons, expected)
