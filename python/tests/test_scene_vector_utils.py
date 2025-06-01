import numpy as np

from isetcam.scene import (
    Scene,
    scene_photons_from_vector,
    scene_energy_from_vector,
)
from isetcam.quanta2energy import quanta_to_energy


def _simple_scene() -> Scene:
    wave = np.array([500, 510, 520])
    photons = np.arange(24).reshape(2, 2, 6)[:, :, :3]  # just ensure shape
    return Scene(photons=photons, wave=wave)


def test_scene_photons_from_vector():
    sc = _simple_scene()
    vec = scene_photons_from_vector(sc, 1, 0)
    expected = sc.photons[1, 0, :].reshape(-1)
    assert np.array_equal(vec, expected)


def test_scene_energy_from_vector():
    sc = _simple_scene()
    vec = scene_energy_from_vector(sc, 0, 1)
    expected = quanta_to_energy(sc.wave, sc.photons[0, 1, :])
    assert np.allclose(vec, expected.reshape(-1))
