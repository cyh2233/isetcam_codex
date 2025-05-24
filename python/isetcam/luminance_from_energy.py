"""Calculate luminance from spectral energy data."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import numpy as np
from scipy.io import loadmat

from .vc_get_image_format import vc_get_image_format
from .iset_root_path import iset_root_path

_DEF_BINWIDTH = 10


def _photopic_luminosity(wave: np.ndarray) -> np.ndarray:
    """Return the photopic luminosity function interpolated to ``wave``."""
    root = iset_root_path()
    fpath = root / 'data' / 'human' / 'luminosity.mat'
    data = loadmat(fpath)
    src_wave = data['wavelength'].ravel()
    V = data['data'].ravel()
    return np.interp(wave, src_wave, V, left=0.0, right=0.0)


def luminance_from_energy(
    energy: np.ndarray, wavelength: np.ndarray, binwidth: Optional[float] = None
) -> np.ndarray:
    """Compute luminance (cd/m^2) from spectral energy.

    Parameters
    ----------
    energy : np.ndarray
        Spectral energy in either RGB or XW format with wavelength along
        the last dimension or columns.
    wavelength : array-like
        Sampled wavelengths in nanometers.
    binwidth : float, optional
        Spectral bin width in nanometers. When not provided, it is derived
        from ``wavelength`` if possible, otherwise defaults to 10 nm.

    Returns
    -------
    np.ndarray
        Luminance values in the same spatial format as ``energy``.
    """
    energy = np.asarray(energy)
    if energy.size == 0:
        return np.array([])

    wavelength = np.asarray(wavelength).reshape(-1)
    if binwidth is None:
        if len(wavelength) > 1:
            binwidth = wavelength[1] - wavelength[0]
        else:
            binwidth = _DEF_BINWIDTH

    img_format = vc_get_image_format(energy, wavelength)
    if img_format == 'RGB':
        n, m, w = energy.shape
        if w != len(wavelength):
            raise ValueError('energy third dimension must be nWave')
        xw = energy.reshape(n * m, w)
    else:
        if energy.ndim == 1:
            xw = energy[np.newaxis, :]
        else:
            xw = energy
        if xw.shape[1] != len(wavelength):
            raise ValueError('Energy must be in XW format with wavelength columns')
        n = m = None

    V = _photopic_luminosity(wavelength)
    lum = 683 * xw.dot(V) * binwidth

    if img_format == 'RGB':
        lum = lum.reshape(n, m)

    return lum
