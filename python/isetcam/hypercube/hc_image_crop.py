"""Crop a region from a hyperspectral cube."""

from __future__ import annotations

from typing import Sequence

import numpy as np


def hc_image_crop(cube: np.ndarray, rect: Sequence[int]) -> np.ndarray:
    """Return ``cube`` cropped to ``rect``.

    ``rect`` is ``(x, y, width, height)`` using 0-based indexing.
    """
    if len(rect) != 4:
        raise ValueError("rect must have four elements")
    x, y, w, h = [int(v) for v in rect]
    if w <= 0 or h <= 0:
        raise ValueError("width and height must be positive")
    if cube.ndim != 3:
        raise ValueError("cube must be 3-D")
    height, width = cube.shape[:2]
    if x < 0 or y < 0 or x + w > width or y + h > height:
        raise ValueError("rect is outside cube bounds")
    return cube[y : y + h, x : x + w, :].copy()

