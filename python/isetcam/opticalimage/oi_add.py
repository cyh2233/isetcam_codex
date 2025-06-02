# mypy: ignore-errors
"""Utilities for combining optical image data."""

from __future__ import annotations

from typing import Sequence, Union, List

import numpy as np

from .oi_class import OpticalImage
from .oi_utils import get_photons, get_n_wave


OpticalImageInput = Union[OpticalImage, Sequence[OpticalImage]]


def _remove_spatial_mean(data: np.ndarray) -> np.ndarray:
    """Remove the mean from each spectral band of ``data``."""
    mean = data.mean(axis=(0, 1), keepdims=True)
    return data - mean


def oi_add(
    in1: OpticalImageInput,
    in2: Union[OpticalImage, Sequence[float]],
    add_flag: str = "add",
) -> OpticalImage:
    """Combine optical images using logic from MATLAB ``oiAdd``.

    Parameters
    ----------
    in1 : OpticalImage or sequence of OpticalImage
        Primary optical image or list of optical images.
    in2 : OpticalImage or sequence of float
        Second optical image to combine with ``in1`` or weights for ``in1``
        when it is a sequence.
    add_flag : {"add", "average", "remove spatial mean"}, optional
        Defines how the optical images are combined.

    Returns
    -------
    OpticalImage
        Resulting optical image with combined photon data.
    """

    flag = add_flag.lower().replace(" ", "")

    # When ``in1`` is a sequence, ``in2`` should be weights
    if isinstance(in1, Sequence) and not isinstance(in1, OpticalImage):
        ois: List[OpticalImage] = list(in1)
        weights = np.asarray(in2, dtype=float)
        if len(weights) != len(ois):
            raise ValueError("Weight vector length must match number of optical images")
        wave = ois[0].wave
        n_wave = get_n_wave(ois[0])
        for oi in ois[1:]:
            if get_n_wave(oi) != n_wave or not np.array_equal(oi.wave, wave):
                raise ValueError("All optical images must share the same wavelength")

        if flag == "average":
            total = np.zeros_like(get_photons(ois[0]), dtype=float)
            for oi in ois:
                total += get_photons(oi)
            photons = total / len(ois)
        else:
            photons = weights[0] * get_photons(ois[0])
            for w, oi in zip(weights[1:], ois[1:]):
                band = get_photons(oi)
                if flag == "removespatialmean":
                    band = _remove_spatial_mean(band)
                elif flag != "add":
                    raise ValueError(f"Unknown add_flag {add_flag}")
                photons += w * band
        return OpticalImage(photons=photons, wave=wave)

    # Pair of optical images
    if not isinstance(in1, OpticalImage) or not isinstance(in2, OpticalImage):
        raise TypeError("in1 and in2 must be OpticalImage instances")
    if not np.array_equal(in1.wave, in2.wave):
        raise ValueError("Optical images must have matching wavelength samples")

    photons1 = get_photons(in1)
    photons2 = get_photons(in2)

    if flag == "add":
        photons = photons1 + photons2
    elif flag == "average":
        photons = (photons1 + photons2) / 2
    elif flag == "removespatialmean":
        photons = photons1 + _remove_spatial_mean(photons2)
    else:
        raise ValueError(f"Unknown add_flag {add_flag}")

    return OpticalImage(photons=photons, wave=in1.wave)
