# mypy: ignore-errors
"""Generate a daylight SPD normalized to 100 cd/m^2."""

from __future__ import annotations

import numpy as np

from .cct_to_sun import cct_to_sun, Units
from .luminance_from_energy import luminance_from_energy
from .luminance_from_photons import luminance_from_photons


_DEF_CCT = 6500


def daylight(wave: np.ndarray, cct: np.ndarray | float = _DEF_CCT, units: Units = "energy") -> np.ndarray:  # noqa: E501
    """Return daylight spectrum scaled to 100 cd/m^2.

    Parameters
    ----------
    wave : array-like
        Sampled wavelengths in nanometers.
    cct : array-like or float, optional
        Correlated color temperature(s) in Kelvin. Defaults to ``6500``.
    units : {"energy", "photons", "quanta"}, optional
        Desired output units. Defaults to ``"energy"``.

    Returns
    -------
    np.ndarray
        Daylight spectral power distribution with shape ``(len(wave), len(cct))``
        or ``(len(wave),)`` when ``cct`` is scalar. The first spectrum has a
        luminance of 100 cd/m^2.
    """
    wave = np.asarray(wave, dtype=float).reshape(-1)
    cct = np.asarray(cct if cct is not None else _DEF_CCT, dtype=float).reshape(-1)

    spd = cct_to_sun(wave, cct, units=units)
    if spd.ndim == 1:
        spd_mat = spd[:, np.newaxis]
    else:
        spd_mat = spd

    if units.lower() in {"photons", "quanta"}:
        lum = luminance_from_photons(spd_mat[:, 0], wave)
    else:
        lum = luminance_from_energy(spd_mat[:, 0], wave)

    if lum == 0:
        scale = 0.0
    else:
        scale = 100.0 / float(lum)
    spd_mat = spd_mat * scale

    if spd_mat.shape[1] == 1:
        return spd_mat[:, 0]
    return spd_mat
