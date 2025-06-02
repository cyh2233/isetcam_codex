# mypy: ignore-errors
"""Convert nonlinear sRGB values to linear RGB."""

from __future__ import annotations

import numpy as np

from .srgb_xyz import srgb_to_linear
from .rgb_to_xw_format import rgb_to_xw_format
from .xw_to_rgb_format import xw_to_rgb_format

__all__ = ["srgb_to_lrgb"]


def srgb_to_lrgb(srgb: np.ndarray) -> np.ndarray:
    """Convert sRGB values to linear RGB.

    Parameters
    ----------
    srgb : np.ndarray
        sRGB values in either ``(n, 3)`` XW format or ``(rows, cols, 3)``
        RGB format.

    Returns
    -------
    np.ndarray
        Linear RGB values in the same spatial format as ``srgb``.
    """
    srgb = np.asarray(srgb, dtype=float)

    if srgb.ndim == 3:
        xw, r, c = rgb_to_xw_format(srgb)
        reshape = True
    elif srgb.ndim == 2 and srgb.shape[1] == 3:
        xw = srgb
        reshape = False
    else:
        raise ValueError("srgb must be (rows, cols, 3) or (n, 3)")

    lrgb = srgb_to_linear(xw)

    if reshape:
        lrgb = xw_to_rgb_format(lrgb, r, c)

    return lrgb
