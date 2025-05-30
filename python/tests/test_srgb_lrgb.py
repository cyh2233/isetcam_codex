import numpy as np

from isetcam import srgb_to_lrgb, lrgb_to_srgb


def test_srgb_lrgb_round_trip_xw():
    srgb = np.random.rand(10, 3)
    lrgb = srgb_to_lrgb(srgb)
    srgb2 = lrgb_to_srgb(lrgb)
    assert np.allclose(srgb2, srgb, atol=1e-6)


def test_srgb_lrgb_round_trip_rgb():
    srgb = np.random.rand(4, 5, 3)
    lrgb = srgb_to_lrgb(srgb)
    srgb2 = lrgb_to_srgb(lrgb)
    assert np.allclose(srgb2, srgb, atol=1e-6)
