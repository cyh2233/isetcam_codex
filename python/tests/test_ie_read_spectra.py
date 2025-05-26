import numpy as np
from scipy.io import loadmat

from isetcam import ie_read_spectra, iset_root_path


def test_ie_read_spectra_interpolation():
    root = iset_root_path()
    path = root / "data" / "lights" / "D65.mat"
    mat = loadmat(path)
    wave = np.arange(400, 701, 10)
    data = np.interp(wave, mat["wavelength"].ravel(), mat["data"].ravel()).reshape(-1, 1)

    res, out_wave, comment, fname = ie_read_spectra(path, wave)
    assert np.array_equal(out_wave, wave)
    assert fname == path
    assert isinstance(comment, str)
    assert res.shape == data.shape
    assert np.allclose(res, data)


def test_ie_read_spectra_extrapolation():
    root = iset_root_path()
    path = root / "data" / "lights" / "D65.mat"
    mat = loadmat(path)
    wave = np.array([295, 300, 320, 835])
    expected = np.interp(
        wave,
        mat["wavelength"].ravel(),
        mat["data"].ravel(),
        left=-1.0,
        right=-1.0,
    ).reshape(-1, 1)
    res, out_wave, _, _ = ie_read_spectra(path, wave, extrap_val=-1.0)
    assert np.array_equal(out_wave, wave)
    assert res.shape == expected.shape
    assert np.allclose(res, expected)
