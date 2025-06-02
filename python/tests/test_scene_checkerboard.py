import numpy as np

from isetcam.scene import scene_checkerboard
from isetcam.illuminant import illuminant_create


def test_scene_checkerboard_size():
    sc = scene_checkerboard(4, 3)
    assert sc.photons.shape[0] == 24
    assert sc.photons.shape[1] == 24
    assert sc.photons.shape[2] == sc.wave.size


def test_scene_checkerboard_spectra():
    sc = scene_checkerboard(1, 1, spectral_type="d65")
    wave = sc.wave
    ill = illuminant_create("D65", wave)
    white = sc.photons[0, 1, :]
    black = sc.photons[0, 0, :]
    assert np.allclose(white, ill.spd)
    assert np.allclose(black, ill.spd * 1e-6)
