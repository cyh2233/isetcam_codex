import numpy as np
from isetcam.scene import Scene, get_photons, set_photons, get_n_wave


def test_scene_accessors():
    wave = np.array([500, 510, 520])
    photons = np.ones((1, 1, 3))
    sc = Scene(photons=photons.copy(), wave=wave)

    assert get_n_wave(sc) == 3
    assert np.allclose(get_photons(sc), photons)

    new_photons = np.zeros_like(photons)
    set_photons(sc, new_photons)
    assert np.allclose(get_photons(sc), new_photons)
