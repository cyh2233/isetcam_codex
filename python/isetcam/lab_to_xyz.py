"""Convert CIE L*a*b* values to CIE XYZ."""

from __future__ import annotations

import numpy as np

from .rgb_to_xw_format import rgb_to_xw_format
from .xw_to_rgb_format import xw_to_rgb_format


_DEF_THRESHOLD = 0.206893

def lab_to_xyz(lab: np.ndarray, whitepoint: np.ndarray) -> np.ndarray:
    """Convert CIE L*a*b* values to XYZ tristimulus values.

    Parameters
    ----------
    lab : np.ndarray
        L*a*b* values in either XW format ``(n, 3)`` or RGB format
        ``(rows, cols, 3)``.
    whitepoint : array-like
        Reference whitepoint as ``(Xn, Yn, Zn)``.

    Returns
    -------
    np.ndarray
        XYZ values in the same spatial format as ``lab``.
    """
    lab = np.asarray(lab, dtype=float)
    wp = np.asarray(whitepoint, dtype=float).reshape(3)
    Xn, Yn, Zn = wp

    if lab.ndim == 3:
        xw, r, c = rgb_to_xw_format(lab)
        reshape = True
    elif lab.ndim == 2:
        if lab.shape[1] != 3:
            raise ValueError("lab must have shape (n,3)")
        xw = lab
        reshape = False
    else:
        raise ValueError("lab must be (n,3) or (rows,cols,3)")

    fy = (xw[:, 0] + 16) / 116
    y = fy ** 3
    yy = xw[:, 0] <= 7.9996
    y[yy] = xw[yy, 0] / 903.3
    fy[yy] = 7.787 * y[yy] + 16 / 116

    fx = xw[:, 1] / 500 + fy
    fz = fy - xw[:, 2] / 200

    xx = fx < _DEF_THRESHOLD
    zz = fz < _DEF_THRESHOLD

    x = fx ** 3
    z = fz ** 3
    x[xx] = (fx[xx] - 16 / 116) / 7.787
    z[zz] = (fz[zz] - 16 / 116) / 7.787

    xyz = np.stack([x * Xn, y * Yn, z * Zn], axis=1)

    if reshape:
        xyz = xw_to_rgb_format(xyz, r, c)
    return xyz
