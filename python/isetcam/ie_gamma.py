# mypy: ignore-errors
"""Apply or remove gamma correction curves."""

from __future__ import annotations

import numpy as np

from .rgb_to_xw_format import rgb_to_xw_format
from .xw_to_rgb_format import xw_to_rgb_format


def ie_gamma(img: np.ndarray, gamma: float | np.ndarray, inverse: bool = False) -> np.ndarray:
    """Apply or remove gamma correction.

    Parameters
    ----------
    img : np.ndarray
        Image data. Can be ``(M, N)`` XW format or ``(R, C, 3)`` RGB.
    gamma : float or array-like
        Scalar gamma exponent or lookup table mapping digital code values
        to linear intensity. When an array is supplied it may be ``(G,)``
        or ``(G, C)`` where ``G`` is the number of table entries and
        ``C`` is either ``1`` or matches the number of image channels.
    inverse : bool, optional
        When ``True`` remove gamma correction using the provided exponent
        or lookup table.

    Returns
    -------
    np.ndarray
        Array with gamma correction applied in the same shape as ``img``.
    """
    arr = np.asarray(img, dtype=float)

    if arr.ndim == 3:
        xw, rows, cols = rgb_to_xw_format(arr)
        reshape = True
    elif arr.ndim == 2:
        xw = arr
        reshape = False
    else:
        raise ValueError("img must be a 2-D or 3-D array")

    if np.isscalar(gamma):
        g = float(gamma)
        if inverse:
            out = xw ** g
        else:
            out = np.clip(xw, 0.0, None) ** (1 / g)
    else:
        tbl = np.asarray(gamma, dtype=float)
        if tbl.ndim == 1:
            tbl = tbl[:, np.newaxis]
        n_levels, g_channels = tbl.shape
        n_channels = xw.shape[1]
        if g_channels == 1 and n_channels > 1:
            tbl = np.tile(tbl, (1, n_channels))
        elif g_channels != n_channels:
            raise ValueError("Gamma table channel mismatch with image")

        out = np.empty_like(xw)
        if inverse:
            inv_levels = np.linspace(0, 1, n_levels)
            for i in range(n_channels):
                out[:, i] = np.interp(xw[:, i], tbl[:, i], inv_levels)
        else:
            if xw.max() <= 1:
                idx = np.round(xw * (n_levels - 1)).astype(int)
            else:
                idx = np.round(xw).astype(int)
            idx = np.clip(idx, 0, n_levels - 1)
            for i in range(n_channels):
                out[:, i] = tbl[idx[:, i], i]

    if reshape:
        out = xw_to_rgb_format(out, rows, cols)

    return out


__all__ = ["ie_gamma"]
