import numpy as np

from isetcam.camera import camera_create, camera_vsnr
from isetcam.scene import Scene
from isetcam.quanta2energy import quanta_to_energy
from isetcam.ie_xyz_from_energy import ie_xyz_from_energy
from isetcam.metrics import xyz_to_vsnr


def _simple_scene(w=2, h=2, n_wave=3) -> Scene:
    wave = np.arange(500, 500 + 10 * n_wave, 10)
    photons = np.arange(w * h * n_wave, dtype=float).reshape((h, w, n_wave))
    return Scene(photons=photons, wave=wave)


def test_camera_vsnr_matches_manual():
    cam = camera_create()
    sc = _simple_scene()
    val = camera_vsnr(cam, sc)

    energy = quanta_to_energy(sc.wave, sc.photons)
    xyz = ie_xyz_from_energy(energy, sc.wave)
    expected = xyz_to_vsnr(xyz, np.array([1.0, 1.0, 1.0]))
    assert np.isclose(val, expected)


def test_camera_vsnr_uniform_scene():
    cam = camera_create()
    wave = np.arange(500, 530, 10)
    photons = np.ones((4, 4, wave.size), dtype=float)
    sc = Scene(photons=photons, wave=wave)
    val = camera_vsnr(cam, sc)
    assert np.isfinite(val)
    assert val > 0
