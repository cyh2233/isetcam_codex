"""Convert CIE xyY values to XYZ tristimulus values."""

from __future__ import annotations

import numpy as np

from .rgb_to_xw_format import rgb_to_xw_format
from .xw_to_rgb_format import xw_to_rgb_format


def xyy_to_xyz(xyy: np.ndarray) -> np.ndarray:
    """Convert xyY coordinates to XYZ tristimulus values.

    Parameters
    ----------
    xyy : np.ndarray
        xyY values in either XW format ``(n, 3)`` or RGB format
        ``(rows, cols, 3)``.

    Returns
    -------
    np.ndarray
        XYZ values in the same spatial format as ``xyy``.
    """
    xyy = np.asarray(xyy, dtype=float)

    if xyy.ndim == 3:
        xw, r, c = rgb_to_xw_format(xyy)
        reshape = True
    elif xyy.ndim == 2 and xyy.shape[1] == 3:
        xw = xyy
        reshape = False
    else:
        raise ValueError("xyy must be (n,3) or (rows,cols,3)")

    xyz = np.zeros_like(xw)
    xyz[:, 1] = xw[:, 2]
    with np.errstate(divide="ignore", invalid="ignore"):
        sXYZ = np.zeros_like(xw[:, 0])
        mask = xw[:, 1] != 0
        sXYZ[mask] = xw[mask, 2] / xw[mask, 1]
        xyz[mask, 0] = (xw[mask, 0] / xw[mask, 1]) * xw[mask, 2]
        xyz[mask, 2] = sXYZ[mask] - xw[mask, 2] - xyz[mask, 0]

    if reshape:
        xyz = xw_to_rgb_format(xyz, r, c)

    return xyz
