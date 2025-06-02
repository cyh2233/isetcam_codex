# mypy: ignore-errors
"""Convert XYZ tristimulus values to CIE xyY."""

from __future__ import annotations

import numpy as np

from .rgb_to_xw_format import rgb_to_xw_format
from .xw_to_rgb_format import xw_to_rgb_format


def xyz_to_xyy(xyz: np.ndarray) -> np.ndarray:
    """Convert XYZ tristimulus values to xyY coordinates.

    Parameters
    ----------
    xyz : np.ndarray
        XYZ values in either XW format ``(n, 3)`` or RGB format
        ``(rows, cols, 3)``.

    Returns
    -------
    np.ndarray
        xyY values in the same spatial format as ``xyz``.
    """
    xyz = np.asarray(xyz, dtype=float)

    if xyz.ndim == 3:
        xw, r, c = rgb_to_xw_format(xyz)
        reshape = True
    elif xyz.ndim == 2 and xyz.shape[1] == 3:
        xw = xyz
        reshape = False
    else:
        raise ValueError("xyz must be (n,3) or (rows,cols,3)")

    s = xw.sum(axis=1)
    xyy = np.zeros_like(xw)
    nz = s != 0
    xyy[nz, 0] = xw[nz, 0] / s[nz]
    xyy[nz, 1] = xw[nz, 1] / s[nz]
    xyy[:, 2] = xw[:, 1]

    if reshape:
        xyy = xw_to_rgb_format(xyy, r, c)

    return xyy
