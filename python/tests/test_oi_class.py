import numpy as np
from isetcam.opticalimage import OpticalImage


def test_oi_repr():
    wave = np.array([400, 500, 600])
    photons = np.zeros((2, 2, 3))
    oi = OpticalImage(photons=photons, wave=wave, name="my oi")
    r = repr(oi)
    assert "my oi" in r
    assert "(2, 2, 3)" in r
    assert "400" in r and "600" in r
