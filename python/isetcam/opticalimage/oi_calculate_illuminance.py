# mypy: ignore-errors
"""Calculate optical image illuminance from photon data."""

from __future__ import annotations

import numpy as np

from .oi_class import OpticalImage
from ..luminance_from_photons import luminance_from_photons


def oi_calculate_illuminance(
    oi: OpticalImage, binwidth: float | None = None
) -> np.ndarray:
    """Return illuminance in lux for each pixel of ``oi``.

    Parameters
    ----------
    oi : OpticalImage
        Optical image providing photon data.
    binwidth : float, optional
        Spectral bin width in nanometers. When not provided it is
        derived from ``oi.wave`` if possible, otherwise defaults to
        10 nm.

    Returns
    -------
    np.ndarray
        Illuminance values in lux with the same spatial dimensions as
        ``oi.photons``.
    """
    photons = np.asarray(oi.photons, dtype=float)
    wave = np.asarray(oi.wave, dtype=float).reshape(-1)

    if photons.shape[-1] != wave.size:
        raise ValueError("oi.photons last dimension must match oi.wave length")

    return luminance_from_photons(photons, wave, binwidth)
