"""Convert energy to photon counts."""

from __future__ import annotations

import numpy as np

from .vc_constants import vc_constants


def energy_to_quanta(wavelength: np.ndarray, energy: np.ndarray) -> np.ndarray:
    """Convert energy to photon counts.

    Parameters
    ----------
    wavelength : array-like
        Sampled wavelengths in nanometers.
    energy : np.ndarray
        Energy values arranged with wavelength along rows. RGB data may be
        provided in ``(height, width, n_wave)`` format.

    Returns
    -------
    np.ndarray
        Photon counts in the same format as ``energy``.
    """
    energy = np.asarray(energy)
    if energy.size == 0:
        return np.array([])

    wavelength = np.asarray(wavelength).reshape(-1)

    h = vc_constants('h')
    c = vc_constants('c')

    if energy.ndim == 3:
        n, m, w = energy.shape
        if w != len(wavelength):
            raise ValueError('energy third dimension must be nWave')
        flat = energy.reshape(n * m, w).T
        photons = (flat / (h * c)) * (1e-9 * wavelength[:, np.newaxis])
        return photons.T.reshape(n, m, w)

    if energy.ndim == 1:
        energy = energy.reshape(len(wavelength), 1)

    n, m = energy.shape
    if n != len(wavelength):
        raise ValueError('energy must have row length equal to numWave')
    return (energy / (h * c)) * (1e-9 * wavelength[:, np.newaxis])
