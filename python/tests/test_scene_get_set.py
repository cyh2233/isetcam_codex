import numpy as np

from isetcam.scene import Scene, scene_get, scene_set
from isetcam.luminance_from_photons import luminance_from_photons
from isetcam.ie_xyz_from_photons import ie_xyz_from_photons


def test_scene_get_set():
    wave = np.array([500, 510, 520])
    photons = np.ones((2, 2, 3))
    sc = Scene(photons=photons.copy(), wave=wave, name="orig")

    assert np.allclose(scene_get(sc, " PhoTonS "), photons)
    assert np.array_equal(scene_get(sc, "WAVE"), wave)
    assert scene_get(sc, "N WAVE") == 3
    assert scene_get(sc, " NAME ") == "orig"

    expected_lum = luminance_from_photons(photons, wave)
    assert np.allclose(scene_get(sc, " LuMiNaNcE"), expected_lum)

    new_photons = np.zeros_like(photons)
    scene_set(sc, " PhoTonS", new_photons)
    assert np.allclose(scene_get(sc, " PHOTONS"), new_photons)

    new_wave = np.array([400, 500])
    scene_set(sc, " WaVe ", new_wave)
    assert np.array_equal(scene_get(sc, "waVe"), new_wave)
    assert scene_get(sc, "N_WAVE") == len(new_wave)

    scene_set(sc, " NaMe", "new")
    assert scene_get(sc, " NAME ") == "new"


def test_scene_get_xyz():
    wave = np.array([500, 510, 520])
    photons = np.ones((1, 1, 3))
    sc = Scene(photons=photons, wave=wave)

    xyz = scene_get(sc, "xyz")
    expected = ie_xyz_from_photons(photons, wave)

    assert xyz.shape == (1, 1, 3)
    assert np.allclose(xyz, expected)
