# mypy: ignore-errors
"""Extract a subset of wavelengths from an :class:`OpticalImage`."""

from __future__ import annotations

from typing import Sequence

import numpy as np

from .oi_class import OpticalImage
from ..luminance_from_photons import luminance_from_photons


def oi_extract_waveband(
    oi: OpticalImage, wave_list: Sequence[float], illuminance: bool = False
) -> OpticalImage:
    """Return a new optical image containing only wavelengths in ``wave_list``.

    Parameters
    ----------
    oi : OpticalImage
        Input optical image to subset.
    wave_list : sequence of float
        Wavelengths in nanometers to extract from ``oi``.
    illuminance : bool, optional
        When ``True``, compute and attach an ``illuminance`` attribute
        based on the extracted photon data.

    Returns
    -------
    OpticalImage
        Optical image with photon data restricted to the requested
        wavelengths.
    """

    wv = np.asarray(oi.wave, dtype=float).reshape(-1)
    target = np.asarray(wave_list, dtype=float).reshape(-1)

    indices = []
    for w in target:
        matches = np.where(np.isclose(wv, w))[0]
        if matches.size == 0:
            raise ValueError(f"Wavelength {w} not found in oi.wave")
        indices.append(matches[0])

    photons = oi.photons[:, :, indices].copy()
    new_wave = wv[indices]
    out = OpticalImage(photons=photons, wave=new_wave, name=oi.name)

    if illuminance:
        out.illuminance = luminance_from_photons(photons, new_wave)

    return out
