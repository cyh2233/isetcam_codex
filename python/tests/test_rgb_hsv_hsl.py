import numpy as np

from isetcam import rgb_to_hsv, hsv_to_rgb, rgb_to_hsl, hsl_to_rgb


def test_rgb_hsv_round_trip():
    rgb = np.random.rand(10, 3)
    hsv = rgb_to_hsv(rgb)
    rgb2 = hsv_to_rgb(hsv)
    assert np.allclose(rgb2, rgb, atol=1e-6)

    rgb_im = np.random.rand(4, 5, 3)
    hsv_im = rgb_to_hsv(rgb_im)
    rgb2_im = hsv_to_rgb(hsv_im)
    assert np.allclose(rgb2_im, rgb_im, atol=1e-6)


def test_rgb_hsl_round_trip():
    rgb = np.random.rand(10, 3)
    hsl = rgb_to_hsl(rgb)
    rgb2 = hsl_to_rgb(hsl)
    assert np.allclose(rgb2, rgb, atol=1e-6)

    rgb_im = np.random.rand(4, 5, 3)
    hsl_im = rgb_to_hsl(rgb_im)
    rgb2_im = hsl_to_rgb(hsl_im)
    assert np.allclose(rgb2_im, rgb_im, atol=1e-6)
