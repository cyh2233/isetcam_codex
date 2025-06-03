# mypy: ignore-errors
"""Apply simple barrel distortion to coordinates."""

from __future__ import annotations

import numpy as np


def optics_barrel_distortion(x: np.ndarray, y: np.ndarray, k1: float) -> tuple[np.ndarray, np.ndarray]:
    """Return distorted ``(x, y)`` coordinates.

    Parameters
    ----------
    x, y : array-like
        Undistorted coordinates (typically normalized to the range ``[-1, 1]``).
    k1 : float
        Radial distortion coefficient. Negative values yield barrel distortion.

    Returns
    -------
    tuple[np.ndarray, np.ndarray]
        Distorted ``(x, y)`` coordinates.
    """
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    r2 = x ** 2 + y ** 2
    factor = 1.0 + k1 * r2
    return x * factor, y * factor


__all__ = ["optics_barrel_distortion"]
