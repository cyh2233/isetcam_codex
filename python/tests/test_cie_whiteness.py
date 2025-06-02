import numpy as np
from isetcam.metrics import cie_whiteness


def test_cie_whiteness_xyz_known():
    Y = 95.0
    x = 0.31
    y = 0.33
    X = Y * x / y
    Z = Y * (1 - x - y) / y
    xyz = np.array([X, Y, Z])
    xn = 0.312740384797229
    yn = 0.3290629143489663
    expected = Y + 800 * (xn - x) + 1700 * (yn - y)
    val = cie_whiteness(xyz)
    assert np.isclose(float(val), expected, atol=1e-6)


def test_cie_whiteness_reflectance_perfect_white():
    import scipy.io
    from isetcam.data_path import data_path

    mat = scipy.io.loadmat(data_path("lights/D65.mat"))
    wave = mat["wavelength"].ravel()
    ill = mat["data"].ravel()
    refl = np.ones_like(ill)
    W = cie_whiteness(reflectance=refl, wavelength=wave, illuminant=ill)
    assert np.isclose(W.item(), 100.0)


def test_cie_whiteness_reflectance_scaled_white():
    import scipy.io
    from isetcam.data_path import data_path

    mat = scipy.io.loadmat(data_path("lights/D65.mat"))
    wave = mat["wavelength"].ravel()
    ill = mat["data"].ravel()
    refl = np.full_like(ill, 0.8)
    W = cie_whiteness(reflectance=refl, wavelength=wave, illuminant=ill)
    assert np.isclose(W.item(), 80.0)
