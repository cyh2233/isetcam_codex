# mypy: ignore-errors
"""Conversion utilities between photons and energy."""

from __future__ import annotations

import numpy as np

from .vc_constants import vc_constants
from .vc_get_image_format import vc_get_image_format


def quanta_to_energy(wavelength: np.ndarray, photons: np.ndarray) -> np.ndarray:
    """Convert photon counts to energy.

    Parameters
    ----------
    wavelength : array-like
        Sampled wavelengths in nanometers.
    photons : np.ndarray
        Photon counts in either RGB or XW format.

    Returns
    -------
    np.ndarray
        Energy values in the same format as ``photons``.
    """
    photons = np.asarray(photons)
    if photons.size == 0:
        return np.array([])

    wavelength = np.asarray(wavelength).reshape(-1)

    h = vc_constants('h')
    c = vc_constants('c')

    img_format = vc_get_image_format(photons, wavelength)
    if img_format == 'RGB':
        n, m, w = photons.shape
        if w != len(wavelength):
            raise ValueError('photons third dimension must be nWave')
        flat = photons.reshape(n * m, w)
        energy = (h * c / 1e-9) * flat / wavelength
        return energy.reshape(n, m, w)

    if img_format == 'XW':
        if photons.ndim == 1:
            photons = photons[np.newaxis, :]
        if photons.shape[1] != len(wavelength):
            raise ValueError('Photons (Quanta) must be in XW format.')
        return (h * c / 1e-9) * photons / wavelength

    raise ValueError('Unknown image format')
