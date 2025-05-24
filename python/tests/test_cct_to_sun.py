import numpy as np
from pathlib import Path
from scipy.io import loadmat

from isetcam import cct_to_sun, energy_to_quanta, iset_root_path


def test_cct_to_sun_matches_d65():
    wave = np.arange(380, 781, 5)
    spd = cct_to_sun(wave, 6500)

    root = iset_root_path()
    d65 = loadmat(root / "data" / "lights" / "D65.mat")
    d_wave = d65["wavelength"].ravel()
    d_spd = d65["data"].ravel()
    ref = np.interp(wave, d_wave, d_spd)

    assert spd.shape == wave.shape
    assert np.allclose(spd, ref, atol=1e-6)


def test_cct_to_sun_photons_multi():
    wave = np.arange(400, 701, 10)
    ccts = np.array([4000, 6500])
    spd_energy = cct_to_sun(wave, ccts, units="energy")
    spd_photons = cct_to_sun(wave, ccts, units="photons")

    assert spd_energy.shape == (len(wave), len(ccts))
    assert spd_photons.shape == spd_energy.shape

    expected = energy_to_quanta(wave, spd_energy)
    assert np.allclose(spd_photons, expected)
