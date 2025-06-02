import numpy as np
import pytest

from isetcam import ie_gamma


def test_ie_gamma_scalar_round_trip():
    img = np.random.rand(5, 5, 3)
    out = ie_gamma(img, 2.2)
    back = ie_gamma(out, 2.2, inverse=True)
    assert np.allclose(img, back, atol=1e-7)


def test_ie_gamma_table_round_trip():
    tbl = np.linspace(0, 1, 512) ** (1 / 2.2)
    img = np.random.rand(10, 3)
    out = ie_gamma(img, tbl)
    back = ie_gamma(out, tbl, inverse=True)
    assert np.allclose(img, back, atol=5e-3)


def test_ie_gamma_table_channel_mismatch():
    tbl = np.random.rand(10, 3)
    img = np.random.rand(4, 2)
    with pytest.raises(ValueError):
        ie_gamma(img, tbl)


