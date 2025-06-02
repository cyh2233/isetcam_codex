# mypy: ignore-errors
"""Convert nonlinear sRGB values to Stockman LMS cone responses."""

from __future__ import annotations

from typing import Optional

import numpy as np

from .srgb_xyz import srgb_to_xyz
from .xyz_to_lms import xyz_to_lms


def srgb_to_lms(
    srgb: np.ndarray,
    cb_type: int = 0,
    white_xyz: Optional[np.ndarray] = None,
    extrap_val: float = 0.0,
) -> np.ndarray:
    """Convert sRGB values to LMS.

    Parameters
    ----------
    srgb : np.ndarray
        sRGB values in either ``(n, 3)`` XW format or ``(rows, cols, 3)`` RGB
        format.
    cb_type : int, optional
        Color blindness simulation type. See :func:`xyz_to_lms`.
    white_xyz : array-like, optional
        White point for color blindness simulation when ``cb_type`` is
        positive.
    extrap_val : float, optional
        Missing cone value when ``cb_type`` is negative.

    Returns
    -------
    np.ndarray
        LMS values in the same spatial format as ``srgb``.
    """
    xyz = srgb_to_xyz(srgb)
    return xyz_to_lms(xyz, cb_type=cb_type, white_xyz=white_xyz, extrap_val=extrap_val)
