# mypy: ignore-errors
"""Convert XYZ values to (u', v') or (u, v) chromaticity coordinates."""

from __future__ import annotations

import numpy as np

from .rgb_to_xw_format import rgb_to_xw_format
from .xw_to_rgb_format import xw_to_rgb_format


def xyz_to_uv(xyz: np.ndarray, mode: str = 'uvprime') -> np.ndarray:
    """Convert CIE XYZ values to uniform chromaticity coordinates.

    Parameters
    ----------
    xyz : np.ndarray
        XYZ values in either ``(n, 3)`` XW format or ``(rows, cols, 3)`` RGB
        format.
    mode : str, optional
        ``'uvprime'`` (default) returns the modern u'v' coordinates. ``'uv'``
        returns the older u,v coordinates.

    Returns
    -------
    np.ndarray
        Chromaticity coordinates in the same spatial format as ``xyz`` with
        last dimension size ``2``.
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

    B = xw[:, 0] + 15 * xw[:, 1] + 3 * xw[:, 2]
    u = np.zeros_like(B)
    v = np.zeros_like(B)
    nz = B > 0
    u[nz] = 4 * xw[nz, 0] / B[nz]
    v[nz] = 9 * xw[nz, 1] / B[nz]

    if mode == 'uv':
        v = v / 1.5
    elif mode != 'uvprime':
        raise ValueError("mode must be 'uvprime' or 'uv'")

    uv = np.stack([u, v], axis=1)

    if reshape:
        uv = xw_to_rgb_format(uv, r, c)

    return uv
