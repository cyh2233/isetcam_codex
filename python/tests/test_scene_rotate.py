import numpy as np
from scipy.ndimage import rotate as nd_rotate

from isetcam.scene import Scene, scene_rotate


def _simple_scene(width: int = 3, height: int = 3, n_wave: int = 1) -> Scene:
    wave = np.arange(400, 400 + 10 * n_wave, 10)
    photons = np.arange(width * height * n_wave, dtype=float).reshape(
        (height, width, n_wave)
    )
    return Scene(photons=photons, wave=wave, name="simple")


def test_scene_rotate_90():
    sc = _simple_scene(2, 3, 1)
    out = scene_rotate(sc, 90)
    expected = np.rot90(sc.photons, axes=(0, 1))
    assert np.array_equal(out.photons, expected)
    assert np.array_equal(out.wave, sc.wave)
    assert out.name == sc.name


def test_scene_rotate_general():
    sc = _simple_scene(3, 3, 1)
    angle = 30
    out = scene_rotate(sc, angle, fill=-1)
    expected = nd_rotate(
        sc.photons,
        angle,
        axes=(1, 0),
        reshape=True,
        order=1,
        mode="constant",
        cval=-1,
    )
    assert np.allclose(out.photons, expected)
    assert np.array_equal(out.wave, sc.wave)
    assert out.name == sc.name
