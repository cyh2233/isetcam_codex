import numpy as np

from isetcam.camera import camera_create, camera_vsnr_sl
from isetcam.camera.camera_vsnr_sl import VSNRSLResult, _base_scene
from isetcam.scene import Scene, scene_adjust_luminance
from isetcam.quanta2energy import quanta_to_energy
from isetcam.ie_xyz_from_energy import ie_xyz_from_energy
from isetcam.metrics import xyz_to_vsnr


def _simple_scene(w=4, h=4, n_wave=3) -> Scene:
    wave = np.arange(500, 500 + 10 * n_wave, 10)
    photons = np.arange(w * h * n_wave, dtype=float).reshape((h, w, n_wave))
    return Scene(photons=photons, wave=wave)


def test_camera_vsnr_sl_matches_manual():
    cam = camera_create()
    levels = np.array([1.0, 10.0, 20.0])
    res = camera_vsnr_sl(cam, levels)
    assert isinstance(res, VSNRSLResult)
    assert np.allclose(res.mean_luminances, levels)

    expected = []
    for lum in levels:
        sc = _base_scene()
        sc = scene_adjust_luminance(sc, "mean", float(lum))
        energy = quanta_to_energy(sc.wave, sc.photons)
        xyz = ie_xyz_from_energy(energy, sc.wave)
        expected.append(xyz_to_vsnr(xyz, np.array([1.0, 1.0, 1.0])))
    assert np.allclose(res.vsnr, expected)
