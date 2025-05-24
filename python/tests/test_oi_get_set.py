import numpy as np

from isetcam.opticalimage import OpticalImage, oi_get, oi_set
from isetcam.luminance_from_photons import luminance_from_photons


def test_oi_get_set():
    wave = np.array([500, 510, 520])
    photons = np.ones((2, 2, 3))
    oi = OpticalImage(photons=photons.copy(), wave=wave, name="orig")

    assert np.allclose(oi_get(oi, "photons"), photons)
    assert np.array_equal(oi_get(oi, "wave"), wave)
    assert oi_get(oi, "n wave") == 3
    assert oi_get(oi, "name") == "orig"

    expected_lum = luminance_from_photons(photons, wave)
    assert np.allclose(oi_get(oi, "luminance"), expected_lum)

    new_photons = np.zeros_like(photons)
    oi_set(oi, "photons", new_photons)
    assert np.allclose(oi_get(oi, "photons"), new_photons)

    new_wave = np.array([400, 500])
    oi_set(oi, "wave", new_wave)
    assert np.array_equal(oi_get(oi, "wave"), new_wave)
    assert oi_get(oi, "n_wave") == len(new_wave)

    oi_set(oi, "name", "new")
    assert oi_get(oi, "name") == "new"
