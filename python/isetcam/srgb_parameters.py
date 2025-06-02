# mypy: ignore-errors
"""Return sRGB chromaticity and white point parameters."""

from __future__ import annotations

import numpy as np

from .xyy_to_xyz import xyy_to_xyz


def srgb_parameters(val: str = "all") -> np.ndarray:
    """Return sRGB display parameters.

    Parameters
    ----------
    val : {'all', 'chromaticity', 'luminance', 'xyywhite', 'XYZwhite'}, optional
        Portion of the parameter matrix to return. Defaults to ``'all'``.

    Returns
    -------
    np.ndarray
        Requested parameters from the sRGB standard.
    """
    srgbP = np.array([
        [0.6400, 0.3000, 0.1500, 0.3127],
        [0.3300, 0.6000, 0.0600, 0.3290],
        [0.2126, 0.7152, 0.0722, 1.0000],
    ], dtype=float)

    val = val.lower()
    if val == "all":
        return srgbP
    if val == "chromaticity":
        return srgbP[0:2, 0:3]
    if val == "luminance":
        return srgbP[2, 0:3]
    if val == "xyywhite":
        return srgbP[:, 3]
    if val == "xyzwhite":
        xyY = srgbP[:, 3]
        return xyy_to_xyz(xyY.reshape(1, 3)).reshape(3)
    raise ValueError(f"Unknown request '{val}'")

