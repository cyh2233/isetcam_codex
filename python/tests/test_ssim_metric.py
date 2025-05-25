import numpy as np
from isetcam.metrics import ssim_metric


def test_ssim_identical():
    img = np.random.rand(8, 8)
    val, s_map = ssim_metric(img, img)
    assert val == 1.0
    assert np.allclose(s_map, 1.0)


def test_ssim_known_difference():
    img1 = np.zeros((8, 8))
    img2 = np.ones((8, 8))
    val, s_map = ssim_metric(img1, img2)
    expected = 9.999000099990002e-05
    assert np.isclose(val, expected)
    assert np.allclose(s_map, expected)


def test_ssim_shape_mismatch():
    img1 = np.zeros((8, 8))
    img2 = np.zeros((8, 9))
    try:
        ssim_metric(img1, img2)
    except ValueError:
        pass
    else:
        raise AssertionError("ValueError not raised for mismatched shapes")
