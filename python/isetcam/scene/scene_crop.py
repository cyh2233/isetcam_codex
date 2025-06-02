# mypy: ignore-errors
"""Crop a region from a :class:`Scene`."""

from __future__ import annotations

from typing import Sequence, Tuple

import numpy as np

from .scene_class import Scene
from .scene_utils import get_photons


def scene_crop(scene: Scene, rect: Sequence[int]) -> Scene:
    """Return a new scene cropped to ``rect``.

    Parameters
    ----------
    scene : Scene
        Input scene to crop.
    rect : sequence of int
        ``(x, y, width, height)`` rectangle describing the crop in pixels.
        ``x`` and ``y`` are the upper-left corner using 0-based indexing.

    Returns
    -------
    Scene
        Scene containing the cropped photon data with the original
        wavelength samples. The returned object includes ``crop_rect`` and
        ``full_size`` attributes describing the crop metadata.
    """

    if len(rect) != 4:
        raise ValueError("rect must have four elements (x, y, width, height)")

    x, y, w, h = [int(v) for v in rect]
    if w <= 0 or h <= 0:
        raise ValueError("width and height must be positive")

    photons = get_photons(scene)
    height, width = photons.shape[:2]

    if x < 0 or y < 0 or x + w > width or y + h > height:
        raise ValueError("rect is outside the scene bounds")

    cropped = photons[y : y + h, x : x + w, :].copy()
    out = Scene(photons=cropped, wave=scene.wave, name=scene.name)
    # Attach metadata about the crop
    out.crop_rect = (x, y, w, h)
    out.full_size = (height, width)
    return out
