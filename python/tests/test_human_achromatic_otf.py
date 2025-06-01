import numpy as np
import pytest

from isetcam.human import human_achromatic_otf


def test_human_achromatic_otf_exp():
    sf = np.arange(0, 51, 10)
    expected = 0.3481 + 0.6519 * np.exp(-0.1212 * sf)
    out = human_achromatic_otf(sf, 'exp')
    assert np.allclose(out, expected)


def test_human_achromatic_otf_dl():
    sf = np.arange(0, 51, 10)
    pupil_d = 3.0
    lam = 555.0
    u0 = pupil_d * np.pi * 1e6 / lam / 180.0
    u_hat = sf / u0
    expected = 2 / np.pi * (np.arccos(u_hat) - u_hat * np.sqrt(1 - u_hat ** 2))
    expected[u_hat >= 1] = 0.0
    out = human_achromatic_otf(sf, 'dl', pupil_d)
    assert np.allclose(out, expected)


def test_human_achromatic_otf_watson():
    sf = np.arange(0, 51, 10)
    pupil_d = 3.0
    u1 = 21.95 - 5.512 * pupil_d + 0.3922 * pupil_d ** 2
    lam = 555.0
    u0 = pupil_d * np.pi * 1e6 / lam / 180.0
    u_hat = sf / u0
    mtf_dl = 2 / np.pi * (np.arccos(u_hat) - u_hat * np.sqrt(1 - u_hat ** 2))
    mtf_dl[u_hat >= 1] = 0.0
    expected = (1 + (sf / u1) ** 2) ** (-0.62) * np.sqrt(mtf_dl)
    out = human_achromatic_otf(sf, 'watson', pupil_d)
    assert np.allclose(out, expected)


def test_human_achromatic_otf_requires_pupil():
    with pytest.raises(ValueError):
        human_achromatic_otf([0, 1], 'dl')
    with pytest.raises(ValueError):
        human_achromatic_otf([0, 1], 'watson')
