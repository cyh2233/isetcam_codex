# mypy: ignore-errors
"""Estimate correlated color temperature from a spectral power distribution."""

from __future__ import annotations

import numpy as np

from .ie_xyz_from_energy import ie_xyz_from_energy
from .xyz_to_uv import xyz_to_uv
from .cct import cct

__all__ = ["spd_to_cct"]


def spd_to_cct(wave: np.ndarray, spd: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Return estimated color temperature and ``uv`` chromaticities.

    Parameters
    ----------
    wave : np.ndarray
        Sampled wavelengths in nanometers.
    spd : np.ndarray
        Spectral power distribution. The first dimension should correspond to
        ``wave``. Multiple SPDs can be provided using additional columns.

    Returns
    -------
    tuple[np.ndarray, np.ndarray]
        The estimated color temperature(s) in Kelvin and the corresponding
        ``(u, v)`` coordinates.
    """
    wave = np.asarray(wave, dtype=float).reshape(-1)
    spd = np.asarray(spd, dtype=float)

    if spd.ndim == 1:
        spd = spd[:, np.newaxis]

    if spd.shape[0] != wave.size:
        if spd.shape[1] == wave.size:
            spd = spd.T
        else:
            raise ValueError("SPD shape does not match wavelength array")

    xyz = ie_xyz_from_energy(spd.T, wave)
    uv = xyz_to_uv(xyz, mode="uv")
    temps = np.array([cct(uv[i].reshape(1, 2)) for i in range(uv.shape[0])])

    return temps.squeeze(), uv
