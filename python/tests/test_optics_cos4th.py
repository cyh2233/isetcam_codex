import numpy as np

from isetcam.optics import optics_cos4th


def test_cos4th_far_field():
    x = np.array([[-1e-3, 0.0, 1e-3]])
    y = np.zeros_like(x)
    img_dist = 0.02
    img_diag = 0.001
    fnum = 4.0
    expected = (img_dist / np.sqrt(img_dist**2 + x**2 + y**2)) ** 4
    out = optics_cos4th(x, y, img_dist, img_diag, fnum)
    assert np.allclose(out, expected)


def test_cos4th_near_field():
    x = np.array([0.0])
    y = np.array([0.001])
    img_dist = 0.01
    img_diag = 0.02
    fnum = 5.6
    magnification = 0.5
    cos_phi = img_dist / np.sqrt(img_dist**2 + x**2 + y**2)
    sin_phi = np.sqrt(1.0 - cos_phi**2)
    tan_phi = sin_phi / cos_phi
    sin_theta = 1.0 / (1.0 + 4.0 * (fnum * (1.0 - magnification)) ** 2)
    cos_theta = np.sqrt(1.0 - sin_theta**2)
    tan_theta = sin_theta / cos_theta
    expected = (
        (np.pi / 2.0)
        * (
            1.0
            - (1.0 - tan_theta**2 + tan_phi**2)
            / np.sqrt(tan_phi**4 + 2 * tan_phi**2 * (1.0 - tan_theta**2) + 1.0 / cos_theta**4)
        )
    )
    expected /= np.pi * sin_theta**2
    out = optics_cos4th(x, y, img_dist, img_diag, fnum, magnification)
    assert np.allclose(out, expected)
