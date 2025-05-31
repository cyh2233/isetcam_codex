"""Generate a daylight spectral power distribution from CCT."""

from __future__ import annotations

from pathlib import Path
from typing import Literal

import numpy as np
from scipy.io import loadmat

from .iset_root_path import iset_root_path
from .energy_to_quanta import energy_to_quanta


_DEF_FILE = "cieDaylightBasis.mat"


def _load_daylight_basis(wave: np.ndarray) -> np.ndarray:
    """Return daylight basis functions interpolated to ``wave``."""
    root = iset_root_path()
    mat = loadmat(root / "data" / "lights" / _DEF_FILE)
    src_wave = mat["wavelength"].ravel()
    data = mat["data"]
    if np.array_equal(wave, src_wave):
        return data.astype(float)

    out = np.zeros((wave.size, data.shape[1]), dtype=float)
    for i in range(data.shape[1]):
        out[:, i] = np.interp(wave, src_wave, data[:, i], left=0.0, right=0.0)
    return out


Units = Literal["energy", "photons", "quanta"]


def cct_to_sun(wave: np.ndarray, cct: np.ndarray | float, units: Units = "energy") -> np.ndarray:  # noqa: E501
    """Return daylight SPD for the given correlated color temperature(s).

    Parameters
    ----------
    wave : array-like
        Sampled wavelengths in nanometers.
    cct : array-like or float
        Correlated color temperature(s) in Kelvin.
    units : {"energy", "photons", "quanta"}, optional
        Desired output units. Defaults to "energy".

    Returns
    -------
    np.ndarray
        Spectral power distribution with shape ``(len(wave), len(cct))`` or
        ``(len(wave),)`` when ``cct`` is scalar.
    """
    wave = np.asarray(wave, dtype=float).reshape(-1)
    cct = np.asarray(cct, dtype=float).reshape(-1)

    mask = np.zeros_like(cct, dtype=int)
    mask[(cct >= 4000) & (cct < 7000)] = 1
    mask[(cct >= 7000) & (cct < 30000)] = 2
    if np.any(mask == 0):
        raise ValueError("CCT must be in the range [4000, 30000)")

    xdt1 = -4.6070e9 / cct**3 + 2.9678e6 / cct**2 + 0.09911e3 / cct + 0.244063
    xdt2 = -2.0064e9 / cct**3 + 1.9018e6 / cct**2 + 0.24748e3 / cct + 0.237040
    xd = np.where(mask == 1, xdt1, xdt2)
    yd = -3.000 * xd**2 + 2.870 * xd - 0.275

    M1 = (-1.3515 - 1.7703 * xd + 5.9114 * yd) / (
        0.0241 + 0.2562 * xd - 0.7341 * yd
    )
    M2 = (0.0300 - 31.4424 * xd + 30.0717 * yd) / (
        0.0241 + 0.2562 * xd - 0.7341 * yd
    )
    basis = _load_daylight_basis(wave)
    spd = basis[:, 1:3] @ np.vstack([M1, M2]) + basis[:, 0][:, np.newaxis]

    if units.lower() in {"photons", "quanta"}:
        spd = energy_to_quanta(wave, spd)

    if spd.shape[1] == 1:
        return spd[:, 0]
    return spd
