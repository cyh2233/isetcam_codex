# mypy: ignore-errors
"""Convert luminance Y to CIE L* (CIELAB/CIELUV)."""

from __future__ import annotations

import numpy as np

from .rgb_to_xw_format import rgb_to_xw_format
from .xw_to_rgb_format import xw_to_rgb_format


_DEF_THRESHOLD = 0.008856


def y_to_lstar(Y: np.ndarray, Yn: float) -> np.ndarray:
    """Convert luminance ``Y`` to L*.

    Parameters
    ----------
    Y : np.ndarray
        Luminance values in either ``(n,)`` XW format or ``(rows, cols)`` RGB
        format.
    Yn : float
        Luminance of the reference white point.

    Returns
    -------
    np.ndarray
        L* values in the same shape as ``Y``.
    """
    Y = np.asarray(Y, dtype=float)
    Yn = float(Yn)

    if Y.ndim == 2:
        xw, r, c = rgb_to_xw_format(Y)
        reshape = True
    elif Y.ndim == 1:
        xw = Y.reshape(-1, 1)
        reshape = False
    else:
        raise ValueError("Y must be 1D or 2D array")

    T = xw[:, 0] / Yn
    L = 116 * np.cbrt(T) - 16
    mask = T < _DEF_THRESHOLD
    L[mask] = 903.3 * T[mask]

    if reshape:
        L = xw_to_rgb_format(L[:, np.newaxis], r, c).reshape(r, c)
    else:
        L = L.reshape(Y.shape)

    return L
