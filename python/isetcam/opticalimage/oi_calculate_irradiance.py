"""Calculate integrated irradiance from an OpticalImage."""

from __future__ import annotations

import numpy as np

from .oi_class import OpticalImage


_DEF_BINWIDTH = 10.0


def oi_calculate_irradiance(
    oi: OpticalImage, binwidth: float | None = None
) -> np.ndarray:
    """Return photon irradiance integrated across wavelength.

    Parameters
    ----------
    oi : OpticalImage
        Input optical image providing photon data.
    binwidth : float, optional
        Spectral bin width in nanometers. When not provided it is
        derived from ``oi.wave`` if possible, otherwise defaults to
        10 nm.

    Returns
    -------
    np.ndarray
        Irradiance in photons/(s m^2) with the same spatial dimensions
        as ``oi.photons``.
    """
    photons = np.asarray(oi.photons, dtype=float)
    wave = np.asarray(oi.wave, dtype=float).reshape(-1)

    if photons.shape[-1] != wave.size:
        raise ValueError("oi.photons last dimension must match oi.wave length")

    if binwidth is None:
        if wave.size > 1:
            binwidth = float(wave[1] - wave[0])
        else:
            binwidth = _DEF_BINWIDTH

    irr = photons.sum(axis=2) * binwidth
    return irr
