import numpy as np

from isetcam.scene import Scene, scene_get, scene_set
from isetcam.luminance_from_photons import luminance_from_photons


def test_scene_get_set():
    wave = np.array([500, 510, 520])
    photons = np.ones((2, 2, 3))
    sc = Scene(photons=photons.copy(), wave=wave, name="orig")

    assert np.allclose(scene_get(sc, "photons"), photons)
    assert np.array_equal(scene_get(sc, "wave"), wave)
    assert scene_get(sc, "n wave") == 3
    assert scene_get(sc, "name") == "orig"

    expected_lum = luminance_from_photons(photons, wave)
    assert np.allclose(scene_get(sc, "luminance"), expected_lum)

    new_photons = np.zeros_like(photons)
    scene_set(sc, "photons", new_photons)
    assert np.allclose(scene_get(sc, "photons"), new_photons)

    new_wave = np.array([400, 500])
    scene_set(sc, "wave", new_wave)
    assert np.array_equal(scene_get(sc, "wave"), new_wave)
    assert scene_get(sc, "n_wave") == len(new_wave)

    scene_set(sc, "name", "new")
    assert scene_get(sc, "name") == "new"
