# mypy: ignore-errors
"""Generate evenly spaced points on a circle."""

from __future__ import annotations

import numpy as np
from typing import Tuple


def circle_points(rad_spacing: float = 2 * np.pi / 60) -> Tuple[np.ndarray, np.ndarray]:
    """Return ``(x, y)`` coordinates of points on a unit circle.

    Parameters
    ----------
    rad_spacing : float, optional
        Angular spacing between consecutive points in radians. Defaults to
        ``2 * np.pi / 60`` which yields 61 samples around the circle.

    Returns
    -------
    Tuple[np.ndarray, np.ndarray]
        Arrays containing the x and y coordinates of the sampled points.
    """
    theta = np.arange(0.0, 2 * np.pi + rad_spacing / 2, rad_spacing)
    if theta[-1] > 2 * np.pi:  # Match MATLAB's 0:spacing:2*pi behavior
        theta = theta[:-1]
    if theta[-1] != 2 * np.pi:
        theta = np.append(theta, 2 * np.pi)

    x = np.cos(theta)
    y = np.sin(theta)
    return x, y
