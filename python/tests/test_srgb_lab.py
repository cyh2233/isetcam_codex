import numpy as np

from isetcam import srgb_to_lab, lab_to_srgb

WHITEPOINT = np.array([0.95047, 1.0, 1.08883])


def test_srgb_lab_round_trip_xw():
    srgb = np.random.rand(10, 3)
    lab = srgb_to_lab(srgb, WHITEPOINT)
    srgb2 = lab_to_srgb(lab, WHITEPOINT)
    assert np.allclose(srgb2, srgb, atol=1e-6)


def test_srgb_lab_round_trip_rgb():
    srgb = np.random.rand(4, 5, 3)
    lab = srgb_to_lab(srgb, WHITEPOINT)
    srgb2 = lab_to_srgb(lab, WHITEPOINT)
    assert np.allclose(srgb2, srgb, atol=1e-6)
