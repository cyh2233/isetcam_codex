# mypy: ignore-errors
"""Apply macular pigment transmittance to an optical image."""

from __future__ import annotations

from pathlib import Path

import numpy as np
from scipy.io import loadmat

from ..data_path import data_path
from ..opticalimage import OpticalImage


def _macular_transmittance(density: float, wave: np.ndarray) -> np.ndarray:
    """Return macular pigment transmittance for ``wave``."""
    mat = loadmat(data_path('human/macularPigment.mat'))
    src_wave = mat['wavelength'].ravel()
    data = mat['data'].ravel()
    unit = np.interp(wave, src_wave, data, left=0.0, right=0.0) / 0.3521
    dens = unit * float(density)
    return 10.0 ** (-dens)


def human_macular_transmittance(
    oi: OpticalImage, density: float = 0.35
) -> OpticalImage:
    """Multiply ``oi`` photon data by macular pigment transmittance."""
    wave = np.asarray(oi.wave, dtype=float)
    trans = _macular_transmittance(density, wave)
    photons = np.asarray(oi.photons, dtype=float)
    shape = [1] * photons.ndim
    shape[-1] = trans.size
    out_photons = photons * trans.reshape(shape)
    return OpticalImage(photons=out_photons, wave=wave, name=oi.name)
