"""Crop a region from an :class:`OpticalImage`."""

from __future__ import annotations

from typing import Sequence

import numpy as np

from .oi_class import OpticalImage
from .oi_utils import get_photons


def oi_crop(oi: OpticalImage, rect: Sequence[int]) -> OpticalImage:
    """Return a new optical image cropped to ``rect``.

    Parameters
    ----------
    oi : OpticalImage
        Input optical image to crop.
    rect : sequence of int
        ``(x, y, width, height)`` rectangle describing the crop in pixels.
        ``x`` and ``y`` are the upper-left corner using 0-based indexing.

    Returns
    -------
    OpticalImage
        Optical image containing the cropped photon data with the original
        wavelength samples. The returned object includes ``crop_rect`` and
        ``full_size`` attributes describing the crop metadata.
    """

    if len(rect) != 4:
        raise ValueError("rect must have four elements (x, y, width, height)")

    x, y, w, h = [int(v) for v in rect]
    if w <= 0 or h <= 0:
        raise ValueError("width and height must be positive")

    photons = get_photons(oi)
    height, width = photons.shape[:2]

    if x < 0 or y < 0 or x + w > width or y + h > height:
        raise ValueError("rect is outside the optical image bounds")

    cropped = photons[y : y + h, x : x + w, :].copy()
    out = OpticalImage(photons=cropped, wave=oi.wave, name=oi.name)
    # Attach metadata about the crop
    out.crop_rect = (x, y, w, h)
    out.full_size = (height, width)
    return out
