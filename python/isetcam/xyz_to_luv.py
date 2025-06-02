# mypy: ignore-errors
"""Convert XYZ values to CIELUV."""

from __future__ import annotations

import numpy as np

from .rgb_to_xw_format import rgb_to_xw_format
from .xw_to_rgb_format import xw_to_rgb_format
from .y_to_lstar import y_to_lstar
from .xyz_to_uv import xyz_to_uv


def xyz_to_luv(xyz: np.ndarray, whitepoint: np.ndarray) -> np.ndarray:
    """Convert CIE XYZ values to CIELUV.

    Parameters
    ----------
    xyz : np.ndarray
        XYZ values in either ``(n, 3)`` XW format or ``(rows, cols, 3)`` RGB
        format.
    whitepoint : array-like
        Reference white point as ``(Xn, Yn, Zn)``.

    Returns
    -------
    np.ndarray
        L*u*v* values in the same spatial format as ``xyz``.
    """
    xyz = np.asarray(xyz, dtype=float)
    wp = np.asarray(whitepoint, dtype=float).reshape(3)

    if xyz.ndim == 3:
        xw, r, c = rgb_to_xw_format(xyz)
        reshape = True
    elif xyz.ndim == 2 and xyz.shape[1] == 3:
        xw = xyz
        reshape = False
    else:
        raise ValueError("xyz must be (n,3) or (rows,cols,3)")

    L = y_to_lstar(xw[:, 1], wp[1]).reshape(-1)
    uv = xyz_to_uv(xw)
    un, vn = xyz_to_uv(wp.reshape(1, 3)).reshape(2)

    luv = np.zeros_like(xw)
    luv[:, 0] = L
    luv[:, 1] = 13 * L * (uv[:, 0] - un)
    luv[:, 2] = 13 * L * (uv[:, 1] - vn)

    if reshape:
        luv = xw_to_rgb_format(luv, r, c)

    return luv
