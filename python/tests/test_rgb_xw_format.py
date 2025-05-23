import numpy as np

from isetcam import rgb_to_xw_format, xw_to_rgb_format


def test_round_trip_rgb_xw():
    rgb = np.arange(24).reshape(2, 3, 4)
    xw, r, c = rgb_to_xw_format(rgb)
    assert xw.shape == (6, 4)
    assert r == 2 and c == 3
    rgb2 = xw_to_rgb_format(xw, r, c)
    assert np.array_equal(rgb2, rgb)


def test_single_band_image():
    rgb = np.arange(4).reshape(2, 2)
    xw, r, c = rgb_to_xw_format(rgb)
    assert xw.shape == (4, 1)
    rgb2 = xw_to_rgb_format(xw, r, c)
    assert rgb2.shape == (2, 2, 1)
    assert np.array_equal(rgb2.squeeze(), rgb)
