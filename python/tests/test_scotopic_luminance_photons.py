import numpy as np

from isetcam import (
    scotopic_luminance_from_energy,
    scotopic_luminance_from_photons,
    energy_to_quanta,
)


def test_scotopic_luminance_from_photons():
    wave = np.arange(400, 701, 10)
    energy = np.ones((1, len(wave)))
    # energy_to_quanta expects wavelength along rows
    photons = energy_to_quanta(wave, energy.T).T
    lum = scotopic_luminance_from_photons(photons, wave)
    expected = scotopic_luminance_from_energy(energy, wave)
    assert np.allclose(lum, expected)
