"""Calculate CIE (x, y) chromaticity coordinates from XYZ."""

from __future__ import annotations

import numpy as np


def chromaticity(XYZ: np.ndarray) -> np.ndarray:
    """Return chromaticity coordinates from XYZ values.

    Parameters
    ----------
    XYZ : np.ndarray
        Array of XYZ values in either XW format ``(n, 3)`` or RGB format
        ``(rows, cols, 3)``.

    Returns
    -------
    np.ndarray
        Chromaticity coordinates with the last dimension of size 2.
    """
    XYZ = np.asarray(XYZ)
    if XYZ.ndim == 2:
        if XYZ.shape[1] != 3:
            raise ValueError("XYZ must have 3 columns")
        s = XYZ.sum(axis=1)
        xy = np.zeros((XYZ.shape[0], 2))
        valid = s != 0
        xy[valid, 0] = XYZ[valid, 0] / s[valid]
        xy[valid, 1] = XYZ[valid, 1] / s[valid]
        return xy
    if XYZ.ndim == 3:
        if XYZ.shape[2] != 3:
            raise ValueError("XYZ must have 3 channels")
        s = XYZ.sum(axis=2)
        xy = np.zeros(XYZ.shape[:2] + (2,))
        valid = s != 0
        xy[..., 0][valid] = XYZ[..., 0][valid] / s[valid]
        xy[..., 1][valid] = XYZ[..., 1][valid] / s[valid]
        return xy
    raise ValueError("XYZ must be (n,3) or (rows,cols,3)")
