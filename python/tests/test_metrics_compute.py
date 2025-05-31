import numpy as np

from isetcam.metrics import metrics_compute, sc_params, delta_e_ab, delta_e_uv, scielab
from isetcam import xyz_to_lab, xyz_to_luv

WHITEPOINT = np.array([0.95047, 1.0, 1.08883])


def test_metrics_compute_cielab():
    img1 = np.array([[[0.5, 0.4, 0.3]]])
    img2 = np.array([[[0.4, 0.4, 0.4]]])
    val = metrics_compute(img1, img2, "cielab", white_point=WHITEPOINT)
    expected = delta_e_ab(xyz_to_lab(img1, WHITEPOINT), xyz_to_lab(img2, WHITEPOINT))
    assert np.allclose(val, expected)


def test_metrics_compute_cieluv():
    img1 = np.array([[[0.1, 0.2, 0.3]]])
    img2 = np.array([[[0.2, 0.1, 0.3]]])
    val = metrics_compute(img1, img2, "cieluv", white_point=WHITEPOINT)
    expected = delta_e_uv(xyz_to_luv(img1, WHITEPOINT), xyz_to_luv(img2, WHITEPOINT))
    assert np.allclose(val, expected)


def test_metrics_compute_mse_rmse():
    a = np.zeros((2, 2), dtype=float)
    b = np.ones((2, 2), dtype=float)
    mse = metrics_compute(a, b, "mse")
    rmse = metrics_compute(a, b, "rmse")
    assert np.allclose(mse, (a - b) ** 2)
    assert np.allclose(rmse, np.abs(a - b))


def test_metrics_compute_psnr():
    a = np.zeros((1, 1), dtype=float)
    b = np.array([[1 / 255]], dtype=float)
    val = metrics_compute(a, b, "psnr")
    from isetcam.metrics import ie_psnr

    expected = ie_psnr(a, b)
    assert np.isclose(val, expected)


def test_metrics_compute_scielab():
    img1 = np.random.rand(2, 2, 3)
    img2 = np.random.rand(2, 2, 3)
    params = sc_params()
    val = metrics_compute(img1, img2, "scielab", white_point=WHITEPOINT, params=params)
    expected = scielab(img1, img2, WHITEPOINT, params)
    assert np.allclose(val, expected)
