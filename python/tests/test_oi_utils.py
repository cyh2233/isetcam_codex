import numpy as np
from isetcam.opticalimage import OpticalImage, get_photons, set_photons, get_n_wave


def test_oi_accessors():
    wave = np.array([500, 510, 520])
    photons = np.ones((1, 1, 3))
    oi = OpticalImage(photons=photons.copy(), wave=wave)

    assert get_n_wave(oi) == 3
    assert np.allclose(get_photons(oi), photons)

    new_photons = np.zeros_like(photons)
    set_photons(oi, new_photons)
    assert np.allclose(get_photons(oi), new_photons)
