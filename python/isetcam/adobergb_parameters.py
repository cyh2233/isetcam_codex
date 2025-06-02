# mypy: ignore-errors
"""Return Adobe RGB chromaticity and white point parameters."""

from __future__ import annotations

import numpy as np

from .xyy_to_xyz import xyy_to_xyz


def adobergb_parameters(val: str = "all") -> np.ndarray:
    """Return Adobe RGB display parameters.

    Parameters
    ----------
    val : {'all', 'chromaticity', 'luminance', 'xyywhite', 'XYZwhite'}, optional
        Portion of the parameter matrix to return. Defaults to ``'all'``.

    Returns
    -------
    np.ndarray
        Requested parameters from the Adobe RGB standard.
    """
    adobergbP = np.array([
        [0.64, 0.21, 0.15, 0.3127],
        [0.33, 0.71, 0.06, 0.3290],
        [47.5744, 100.3776, 12.0320, 160.0],
    ], dtype=float)

    val = val.lower()
    if val == "all":
        return adobergbP
    if val == "chromaticity":
        return adobergbP[0:2, 0:3]
    if val == "luminance":
        return adobergbP[2, 0:3]
    if val == "xyywhite":
        return adobergbP[:, 3]
    if val == "xyzwhite":
        xyY = adobergbP[:, 3]
        return xyy_to_xyz(xyY.reshape(1, 3)).reshape(3)
    raise ValueError(f"Unknown request '{val}'")

