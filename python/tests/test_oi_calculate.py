import numpy as np
from scipy.io import loadmat

from isetcam.opticalimage import (
    OpticalImage,
    oi_calculate_irradiance,
    oi_calculate_illuminance,
)
from isetcam import quanta_to_energy, data_path


def _expected_irradiance(wave, photons):
    bw = wave[1] - wave[0] if len(wave) > 1 else 10
    return photons.sum(axis=2) * bw


def _expected_illuminance(wave, photons):
    energy = quanta_to_energy(wave, photons)
    mat = loadmat(data_path("human/luminosity.mat"))
    V = np.interp(wave, mat["wavelength"].ravel(), mat["data"].ravel(), left=0.0, right=0.0)
    bw = wave[1] - wave[0] if len(wave) > 1 else 10
    xw = energy.reshape(-1, len(wave))
    lum = 683 * xw.dot(V) * bw
    return lum.reshape(photons.shape[:2])


def _simple_oi(scale: float = 1.0) -> OpticalImage:
    wave = np.array([500, 510, 520], dtype=float)
    photons = np.ones((2, 2, 3), dtype=float) * scale
    return OpticalImage(photons=photons, wave=wave)


def test_oi_calculate_irradiance():
    oi = _simple_oi(2.0)
    irr = oi_calculate_irradiance(oi)
    expected = _expected_irradiance(oi.wave, oi.photons)
    assert np.allclose(irr, expected)


def test_oi_calculate_illuminance():
    oi = _simple_oi(0.5)
    illum = oi_calculate_illuminance(oi)
    expected = _expected_illuminance(oi.wave, oi.photons)
    assert np.allclose(illum, expected)
