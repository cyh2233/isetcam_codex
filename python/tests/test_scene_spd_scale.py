import numpy as np

from isetcam.scene import Scene, scene_spd_scale


def _simple_scene() -> Scene:
    wave = np.array([500, 510])
    photons = np.arange(8, dtype=float).reshape((2, 2, 2))
    return Scene(photons=photons, wave=wave, name="orig")


def test_scene_spd_scale_basic():
    sc = _simple_scene()
    scale = 2.5
    out = scene_spd_scale(sc, scale)
    assert np.allclose(out.photons, sc.photons * scale)
    assert np.array_equal(out.wave, sc.wave)
    assert out.name != sc.name
    assert str(scale) in out.name
