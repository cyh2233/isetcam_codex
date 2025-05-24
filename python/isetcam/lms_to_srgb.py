"""Convert LMS cone responses to nonlinear sRGB values."""

from __future__ import annotations

import numpy as np

from .lms_to_xyz import lms_to_xyz
from .srgb_xyz import xyz_to_srgb


def lms_to_srgb(lms: np.ndarray) -> np.ndarray:
    """Convert LMS values to sRGB.

    Parameters
    ----------
    lms : np.ndarray
        LMS values in either ``(n, 3)`` XW format or ``(rows, cols, 3)`` RGB
        format.

    Returns
    -------
    np.ndarray
        sRGB values in the same spatial format as ``lms``.
    """
    xyz = lms_to_xyz(lms)
    srgb, _, _ = xyz_to_srgb(xyz)
    return srgb
