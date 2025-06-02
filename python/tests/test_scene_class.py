import numpy as np
from isetcam.scene import Scene


def test_scene_repr():
    wave = np.array([400, 500, 600])
    photons = np.zeros((2, 2, 3))
    sc = Scene(photons=photons, wave=wave, name="my scene")
    r = repr(sc)
    assert "my scene" in r
    assert "(2, 2, 3)" in r
    assert "400" in r and "600" in r
