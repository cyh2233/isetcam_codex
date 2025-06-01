import numpy as np

from isetcam.scene import Scene, scene_radiance_from_vector
from isetcam.quanta2energy import quanta_to_energy


def _simple_scene() -> Scene:
    wave = np.array([500, 510, 520])
    photons = np.arange(24).reshape(2, 2, 6)[:, :, :3]
    return Scene(photons=photons, wave=wave)


def test_scene_radiance_from_vector():
    sc = _simple_scene()
    vec = scene_radiance_from_vector(sc, 1, 1)
    expected = quanta_to_energy(sc.wave, sc.photons[1, 1, :])
    assert vec.shape == (3,)
    assert np.allclose(vec, expected.reshape(-1))

