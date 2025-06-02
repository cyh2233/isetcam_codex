# mypy: ignore-errors
"""Estimate correlated color temperature from XYZ values."""

from __future__ import annotations

import numpy as np

from .xyz_to_uv import xyz_to_uv
from .cct import cct
from .rgb_to_xw_format import rgb_to_xw_format

__all__ = ["xyz_to_cct"]


def xyz_to_cct(xyz: np.ndarray) -> np.ndarray:
    """Return estimated correlated color temperature from XYZ tristimulus values.

    Parameters
    ----------
    xyz : np.ndarray
        XYZ values in either ``(n, 3)`` XW format or ``(rows, cols, 3)`` RGB
        format.

    Returns
    -------
    np.ndarray
        Estimated color temperature(s) in Kelvin with the same spatial
        dimensions as the input (minus the color dimension).
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

    uv = xyz_to_uv(xw, mode="uv")
    temps = np.array([cct(uv[i].reshape(1, 2)) for i in range(uv.shape[0])])

    if reshape:
        temps = temps.reshape(r, c)
    return temps
