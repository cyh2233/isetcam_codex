# mypy: ignore-errors
"""Blur a hyperspectral cube with a Gaussian kernel."""

from __future__ import annotations

import numpy as np
from scipy.ndimage import gaussian_filter


def hc_blur(cube: np.ndarray, sigma: float) -> np.ndarray:
    """Return a blurred copy of ``cube`` using a Gaussian kernel."""
    cube = np.asarray(cube, dtype=float)
    if cube.ndim != 3:
        raise ValueError("cube must be 3-D")

    blurred = np.empty_like(cube)
    for b in range(cube.shape[2]):
        blurred[:, :, b] = gaussian_filter(cube[:, :, b], sigma)
    return blurred

