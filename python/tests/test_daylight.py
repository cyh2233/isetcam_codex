import numpy as np
from scipy.io import loadmat

from isetcam import daylight, energy_to_quanta, luminance_from_energy, data_path


def _expected_d65(wave: np.ndarray) -> np.ndarray:
    mat = loadmat(data_path("lights/D65.mat"))
    d_wave = mat["wavelength"].ravel()
    d_spd = np.interp(wave, d_wave, mat["data"].ravel())
    lum = luminance_from_energy(d_spd[np.newaxis, :], wave)[0]
    return d_spd / lum * 100.0


def test_daylight_matches_matlab_d65():
    wave = np.arange(400, 701, 10)
    spd = daylight(wave, 6500)
    expected = _expected_d65(wave)
    assert spd.shape == wave.shape
    assert np.allclose(spd, expected, atol=1e-6)


def test_daylight_photons_multi():
    wave = np.arange(420, 681, 20)
    ccts = np.array([4000, 6500])
    spd_energy = daylight(wave, ccts, units="energy")
    spd_photons = daylight(wave, ccts, units="photons")

    assert spd_energy.shape == (len(wave), len(ccts))
    assert spd_photons.shape == spd_energy.shape
    expected = energy_to_quanta(wave, spd_energy)
    assert np.allclose(spd_photons, expected)
