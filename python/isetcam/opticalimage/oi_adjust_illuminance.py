"""Adjust optical image illuminance by scaling photon data."""

from __future__ import annotations

import numpy as np

from .oi_class import OpticalImage
from ..luminance_from_photons import luminance_from_photons


def oi_adjust_illuminance(oi: OpticalImage, new_illuminance: float) -> OpticalImage:
    """Scale ``oi`` so the mean illuminance equals ``new_illuminance``.

    Parameters
    ----------
    oi : OpticalImage
        Input optical image to scale.
    new_illuminance : float
        Desired mean illuminance level in lux.

    Returns
    -------
    OpticalImage
        New optical image with scaled photon data.
    """

    photons = np.asarray(oi.photons, dtype=float)
    illum = luminance_from_photons(photons, oi.wave)
    current = float(illum.mean())

    if current > 0:
        photons = photons * (new_illuminance / current)

    return OpticalImage(photons=photons, wave=oi.wave, name=oi.name)
