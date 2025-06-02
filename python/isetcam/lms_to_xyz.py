# mypy: ignore-errors
"""Convert Stockman LMS cone responses to CIE XYZ."""

from __future__ import annotations

import numpy as np

from .rgb_to_xw_format import rgb_to_xw_format
from .xw_to_rgb_format import xw_to_rgb_format

# Matrix converting LMS to XYZ (Stockman cone fundamentals)
_LMS2XYZ = np.array([
    [1.7910, -1.2884, 0.3702],
    [0.6068, 0.4097, -0.0398],
    [-0.0432, 0.0697, 1.8340],
])


def lms_to_xyz(lms: np.ndarray) -> np.ndarray:
    """Convert Stockman LMS cone responses to CIE XYZ values.

    Parameters
    ----------
    lms : np.ndarray
        LMS values in either ``(n, 3)`` XW format or ``(rows, cols, 3)``
        RGB format.

    Returns
    -------
    np.ndarray
        XYZ values in the same spatial format as ``lms``.
    """
    lms = np.asarray(lms, dtype=float)

    if lms.ndim == 3:
        xw, r, c = rgb_to_xw_format(lms)
        reshape = True
    elif lms.ndim == 2 and lms.shape[1] == 3:
        xw = lms
        reshape = False
    else:
        raise ValueError("lms must be (rows, cols, 3) or (n, 3)")

    xyz = xw @ _LMS2XYZ

    if reshape:
        xyz = xw_to_rgb_format(xyz, r, c)

    return xyz
