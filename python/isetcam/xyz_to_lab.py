# mypy: ignore-errors
"""Convert CIE XYZ values to CIE L*a*b*."""

from __future__ import annotations

import numpy as np

from .rgb_to_xw_format import rgb_to_xw_format
from .xw_to_rgb_format import xw_to_rgb_format


_DEF_THRESHOLD = 0.008856


def xyz_to_lab(xyz: np.ndarray, whitepoint: np.ndarray) -> np.ndarray:
    """Convert XYZ tristimulus values to CIE L*a*b*.

    Parameters
    ----------
    xyz : np.ndarray
        XYZ values in either XW format ``(n, 3)`` or RGB format
        ``(rows, cols, 3)``.
    whitepoint : array-like
        Reference whitepoint as ``(Xn, Yn, Zn)``.

    Returns
    -------
    np.ndarray
        L*a*b* values in the same spatial format as ``xyz``.
    """
    xyz = np.asarray(xyz, dtype=float)
    wp = np.asarray(whitepoint, dtype=float).reshape(3)
    Xn, Yn, Zn = wp

    if xyz.ndim == 3:
        xw, r, c = rgb_to_xw_format(xyz)
        reshape = True
    elif xyz.ndim == 2:
        if xyz.shape[1] != 3:
            raise ValueError("xyz must have shape (n,3)")
        xw = xyz
        reshape = False
    else:
        raise ValueError("xyz must be (n,3) or (rows,cols,3)")

    x = xw[:, 0] / Xn
    y = xw[:, 1] / Yn
    z = xw[:, 2] / Zn

    lab = np.zeros_like(xw)

    yy = y <= _DEF_THRESHOLD
    xx = x <= _DEF_THRESHOLD
    zz = z <= _DEF_THRESHOLD

    fy_small = y[yy]

    y_cbrt = np.cbrt(y)
    lab[:, 0] = 116 * y_cbrt - 16
    lab[yy, 0] = 903.3 * fy_small

    fx = 7.787 * x[xx] + 16 / 116
    fy = 7.787 * fy_small + 16 / 116
    fz = 7.787 * z[zz] + 16 / 116

    x_cbrt = np.cbrt(x)
    z_cbrt = np.cbrt(z)
    x_cbrt[xx] = fx
    y_cbrt[yy] = fy
    z_cbrt[zz] = fz

    lab[:, 1] = 500 * (x_cbrt - y_cbrt)
    lab[:, 2] = 200 * (y_cbrt - z_cbrt)

    if reshape:
        lab = xw_to_rgb_format(lab, r, c)
    return lab
