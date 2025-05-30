import numpy as np

from isetcam.camera import camera_create, camera_mtf, camera_acutance
from isetcam.camera.camera_acutance import _freq_to_cpd
from isetcam.metrics import iso_acutance


def test_camera_acutance_matches_manual():
    cam = camera_create()
    freqs, mtf = camera_mtf(cam)
    cpd = _freq_to_cpd(freqs, cam.optics.f_length)
    expected = iso_acutance(cpd, mtf)
    val = camera_acutance(cam)
    assert np.isclose(val, expected)
