import numpy as np
from isetcam import ie_psnr


def test_ie_psnr_basic():
    img1 = np.zeros((4, 4), dtype=float)
    img2 = np.zeros((4, 4), dtype=float)
    assert np.isinf(ie_psnr(img1, img2))


def test_ie_psnr_known_value():
    img1 = np.zeros((1, 1), dtype=float)
    img2 = np.array([[1 / 255]], dtype=float)
    val = ie_psnr(img1, img2)
    expected = 20 * np.log10(255)
    assert np.isclose(val, expected)


def test_ie_psnr_additional_difference():
    img1 = np.zeros((1, 1), dtype=float)
    img2 = np.array([[2 / 255]], dtype=float)
    val = ie_psnr(img1, img2)
    expected = 20 * np.log10(255 / 2)
    assert np.isclose(val, expected)
