import numpy as np
from scipy.ndimage import rotate as nd_rotate

from isetcam import (
    image_flip,
    image_rotate,
    image_translate,
    image_crop_border,
    ie_lut_digital,
    ie_lut_linear,
    ie_lut_invert,
)


def test_image_flip():
    img = np.arange(6).reshape(2, 3)
    assert np.array_equal(image_flip(img, "updown"), np.flip(img, axis=0))
    assert np.array_equal(image_flip(img, "leftRight"), np.flip(img, axis=1))


def test_image_rotate():
    img = np.arange(6).reshape(2, 3)
    out = image_rotate(img, "cw")
    assert np.array_equal(out, np.rot90(img, -1))
    angle = 30
    out = image_rotate(img, angle, fill=-1)
    expected = nd_rotate(img, angle, axes=(1, 0), reshape=True, order=1, mode="constant", cval=-1)
    assert np.allclose(out, expected)


def test_image_translate():
    img = np.arange(9).reshape(3, 3)
    out = image_translate(img, 1, 1, fill=-1)
    expected = np.full_like(img, -1)
    expected[1:, 1:] = img[:-1, :-1]
    assert np.array_equal(out, expected)


def test_ie_lut_scalar():
    img = np.array([[0, 1]], dtype=float)
    digital = ie_lut_linear(img, 2)
    assert np.allclose(digital, img ** 0.5)
    rgb = ie_lut_digital(digital, 2)
    assert np.allclose(rgb, img)


def test_ie_lut_invert():
    table = np.linspace(0, 1, 4)[:, None]
    inv = ie_lut_invert(table, 4)
    assert inv.shape == (4, 1)
    assert np.allclose(inv[:, 0], np.linspace(1, 4, 4))


def test_image_crop_border():
    img = np.zeros((5, 5))
    img[1:4, 1:4] = 1
    cropped = image_crop_border(img, threshold=0.1)
    assert cropped.shape == (3, 3)
    assert np.allclose(cropped, 1)

