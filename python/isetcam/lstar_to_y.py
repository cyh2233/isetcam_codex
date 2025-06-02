# mypy: ignore-errors
"""Convert CIE L* (CIELAB/CIELUV) to luminance Y."""

from __future__ import annotations

import numpy as np

from .rgb_to_xw_format import rgb_to_xw_format
from .xw_to_rgb_format import xw_to_rgb_format


# Threshold for switching formula based on L* value
_LSTAR_THRESHOLD = 7.9996


def lstar_to_y(L: np.ndarray, Yn: float) -> np.ndarray:
    """Convert L* values to luminance ``Y``.

    Parameters
    ----------
    L : np.ndarray
        L* values in either ``(n,)`` XW format or ``(rows, cols)`` RGB
        format.
    Yn : float
        Luminance of the reference white point.

    Returns
    -------
    np.ndarray
        Luminance values in the same shape as ``L``.
    """
    L = np.asarray(L, dtype=float)
    Yn = float(Yn)

    if L.ndim == 2:
        xw, r, c = rgb_to_xw_format(L)
        reshape = True
    elif L.ndim == 1:
        xw = L.reshape(-1, 1)
        reshape = False
    else:
        raise ValueError("L must be 1D or 2D array")

    vals = xw[:, 0]
    Y = np.empty_like(vals)

    mask = vals > _LSTAR_THRESHOLD
    Y[mask] = Yn * ((vals[mask] + 16) / 116) ** 3
    Y[~mask] = Yn * vals[~mask] / 903.3

    if reshape:
        Y = xw_to_rgb_format(Y[:, np.newaxis], r, c).reshape(r, c)
    else:
        Y = Y.reshape(L.shape)

    return Y
