import numpy as np
from pathlib import Path
from scipy.io import loadmat

from isetcam import (
    luminance_from_energy,
    luminance_from_photons,
    energy_to_quanta,
)


def _expected_luminance(wave, energy):
    root = Path(__file__).resolve().parents[2]
    mat = loadmat(root / 'data' / 'human' / 'luminosity.mat')
    V = np.interp(wave, mat['wavelength'].ravel(), mat['data'].ravel(), left=0.0, right=0.0)
    binwidth = wave[1] - wave[0] if len(wave) > 1 else 10
    xw = energy.reshape(-1, len(wave))
    lum = 683 * xw.dot(V) * binwidth
    return lum.reshape(energy.shape[:-1])


def test_luminance_from_energy_xw():
    wave = np.arange(400, 701, 10)
    energy = np.ones((1, len(wave)))
    lum = luminance_from_energy(energy, wave)
    expected = _expected_luminance(wave, energy)
    assert np.allclose(lum, expected)


def test_luminance_from_energy_rgb():
    wave = np.arange(400, 701, 10)
    energy = np.ones((1, 1, len(wave)))
    lum = luminance_from_energy(energy, wave)
    expected = _expected_luminance(wave, energy.reshape(1, len(wave)))
    assert np.allclose(lum, expected.reshape(1, 1))


def test_luminance_from_photons():
    wave = np.arange(400, 701, 10)
    energy = np.ones((1, len(wave)))
    # energy_to_quanta expects wavelength along rows
    photons = energy_to_quanta(wave, energy.T).T
    lum = luminance_from_photons(photons, wave)
    expected = _expected_luminance(wave, energy)
    assert np.allclose(lum, expected)
