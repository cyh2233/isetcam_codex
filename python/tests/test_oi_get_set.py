import numpy as np

from isetcam.opticalimage import OpticalImage, oi_get, oi_set
from isetcam.luminance_from_photons import luminance_from_photons


def test_oi_get_set():
    wave = np.array([500, 510, 520])
    photons = np.ones((2, 2, 3))
    oi = OpticalImage(photons=photons.copy(), wave=wave, name="orig")

    assert np.allclose(oi_get(oi, "PHOTONS"), photons)
    assert np.array_equal(oi_get(oi, " wAvE"), wave)
    assert oi_get(oi, "N WAVE") == 3
    assert oi_get(oi, " NAme ") == "orig"

    expected_lum = luminance_from_photons(photons, wave)
    assert np.allclose(oi_get(oi, " LUMINANCE"), expected_lum)

    new_photons = np.zeros_like(photons)
    oi_set(oi, " PhoTonS", new_photons)
    assert np.allclose(oi_get(oi, " phOtOnS"), new_photons)

    new_wave = np.array([400, 500])
    oi_set(oi, "WAVE", new_wave)
    assert np.array_equal(oi_get(oi, " WAVE"), new_wave)
    assert oi_get(oi, "N_WAVE") == len(new_wave)

    oi_set(oi, " NaMe ", "new")
    assert oi_get(oi, "Name" ) == "new"
