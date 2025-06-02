# mypy: ignore-errors
"""Convert blackbody color temperature to sRGB."""

from __future__ import annotations

import numpy as np

from .illuminant import illuminant_blackbody
from .ie_xyz_from_energy import ie_xyz_from_energy
from .srgb_xyz import xyz_to_srgb

__all__ = ["ctemp_to_srgb"]


def ctemp_to_srgb(temp: float | np.ndarray, wave: np.ndarray | None = None) -> np.ndarray:  # noqa: E501
    """Return sRGB value for a blackbody at the given color temperature.

    Parameters
    ----------
    temp : float or array-like
        Blackbody color temperature(s) in Kelvin.
    wave : array-like, optional
        Sampled wavelengths in nanometers. Defaults to 400-700 nm in 10 nm steps.

    Returns
    -------
    np.ndarray
        sRGB values for each temperature. Shape is ``(n, 3)`` where ``n`` is the
        number of temperatures, or ``(3,)`` when ``temp`` is scalar.
    """
    if wave is None:
        wave = np.arange(400, 701, 10)
    wave = np.asarray(wave, dtype=float).reshape(-1)
    temps = np.asarray(temp, dtype=float).reshape(-1)

    spd = np.stack([illuminant_blackbody(t, wave) for t in temps], axis=0)
    xyz = ie_xyz_from_energy(spd, wave)
    srgb, _, _ = xyz_to_srgb(xyz)

    if srgb.shape[0] == 1:
        return srgb[0]
    return srgb

