# mypy: ignore-errors
"""Convert linear RGB values to nonlinear sRGB."""

from __future__ import annotations

import numpy as np

from .srgb_xyz import linear_to_srgb
from .rgb_to_xw_format import rgb_to_xw_format
from .xw_to_rgb_format import xw_to_rgb_format

__all__ = ["lrgb_to_srgb"]


def lrgb_to_srgb(lrgb: np.ndarray) -> np.ndarray:
    """Convert linear RGB values to sRGB.

    Parameters
    ----------
    lrgb : np.ndarray
        Linear RGB values in either ``(n, 3)`` XW format or ``(rows, cols, 3)``
        RGB format. Values should be in ``[0, 1]``.

    Returns
    -------
    np.ndarray
        sRGB values in the same spatial format as ``lrgb``.
    """
    lrgb = np.asarray(lrgb, dtype=float)

    if lrgb.max() > 1 or lrgb.min() < 0:
        raise ValueError("lrgb values must be between 0 and 1")

    if lrgb.ndim == 3:
        xw, r, c = rgb_to_xw_format(lrgb)
        reshape = True
    elif lrgb.ndim == 2 and lrgb.shape[1] == 3:
        xw = lrgb
        reshape = False
    else:
        raise ValueError("lrgb must be (rows, cols, 3) or (n, 3)")

    srgb = linear_to_srgb(xw)

    if reshape:
        srgb = xw_to_rgb_format(srgb, r, c)

    return srgb
