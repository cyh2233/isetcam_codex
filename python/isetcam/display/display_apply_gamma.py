# mypy: ignore-errors
"""Apply display gamma curves."""

from __future__ import annotations

import numpy as np

from .display_class import Display
from ..rgb_to_xw_format import rgb_to_xw_format
from ..xw_to_rgb_format import xw_to_rgb_format


def display_apply_gamma(img: np.ndarray, display: Display, inverse: bool = False) -> np.ndarray:  # noqa: E501
    """Apply forward or inverse gamma correction using ``display.gamma``.

    Parameters
    ----------
    img : np.ndarray
        Image data in either ``(R, C, N)`` RGB or ``(M, N)`` XW format.
    display : Display
        Display object providing the gamma table.
    inverse : bool, optional
        When ``True``, apply the inverse gamma mapping (linear to digital).

    Returns
    -------
    np.ndarray
        Gamma corrected image in the same shape as ``img``.
    """
    if display.gamma is None:
        raise ValueError("Display has no gamma table")

    img = np.asarray(img, dtype=float)

    if img.ndim == 3:
        xw, rows, cols = rgb_to_xw_format(img)
        reshape = True
    elif img.ndim == 2:
        xw = img
        reshape = False
    else:
        raise ValueError("img must be a 2D or 3D array")

    gamma = np.asarray(display.gamma, dtype=float)
    if gamma.ndim == 1:
        gamma = gamma.reshape(-1, 1)

    n_levels, g_channels = gamma.shape
    n_channels = xw.shape[1]

    if g_channels == 1 and n_channels > 1:
        gamma = np.tile(gamma, (1, n_channels))
    elif g_channels != n_channels:
        raise ValueError("Gamma table channel mismatch with image")

    out = np.empty_like(xw)

    if inverse:
        inv_levels = np.linspace(0, 1, n_levels)
        for i in range(n_channels):
            out[:, i] = np.interp(xw[:, i], gamma[:, i], inv_levels)
    else:
        if xw.max() <= 1:
            idx = np.round(xw * (n_levels - 1)).astype(int)
        else:
            idx = np.round(xw).astype(int)
        idx = np.clip(idx, 0, n_levels - 1)
        for i in range(n_channels):
            out[:, i] = gamma[idx[:, i], i]

    if reshape:
        out = xw_to_rgb_format(out, rows, cols)

    return out
