import numpy as np

from isetcam import rgb_to_ycbcr, ycbcr_to_rgb


def test_rgb_ycbcr_round_trip_xw():
    rgb = np.random.rand(10, 3)
    ycbcr = rgb_to_ycbcr(rgb)
    rgb2 = ycbcr_to_rgb(ycbcr)
    assert np.allclose(rgb2, rgb, atol=1e-6)


def test_rgb_ycbcr_round_trip_rgb():
    rgb = np.random.rand(4, 5, 3)
    ycbcr = rgb_to_ycbcr(rgb)
    rgb2 = ycbcr_to_rgb(ycbcr)
    assert np.allclose(rgb2, rgb, atol=1e-6)
