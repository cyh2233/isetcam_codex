"""Convert CIE L*a*b* values to nonlinear sRGB."""

from __future__ import annotations

import numpy as np

from .lab_to_xyz import lab_to_xyz
from .srgb_xyz import xyz_to_srgb


def lab_to_srgb(lab: np.ndarray, whitepoint: np.ndarray) -> np.ndarray:
    """Convert L*a*b* values to sRGB.

    Parameters
    ----------
    lab : np.ndarray
        L*a*b* values in either ``(n, 3)`` XW format or ``(rows, cols, 3)`` RGB
        format.
    whitepoint : array-like
        Reference white point as ``(Xn, Yn, Zn)``.

    Returns
    -------
    np.ndarray
        sRGB values in the same spatial format as ``lab``.
    """
    xyz = lab_to_xyz(lab, whitepoint)
    srgb, _, _ = xyz_to_srgb(xyz)
    return srgb
