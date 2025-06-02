# mypy: ignore-errors
"""Rotate a hyperspectral cube and clip to original size."""

from __future__ import annotations

import numpy as np
from scipy.ndimage import rotate as nd_rotate


def hc_image_rotate_clip(cube: np.ndarray, angle: float, fill: float = 0) -> np.ndarray:
    """Return ``cube`` rotated by ``angle`` degrees clipped to original size."""
    cube = np.asarray(cube, dtype=float)
    if cube.ndim != 3:
        raise ValueError("cube must be 3-D")
    rotated = nd_rotate(
        cube,
        angle,
        axes=(1, 0),
        reshape=False,
        order=1,
        mode="constant",
        cval=float(fill),
    )
    return rotated

