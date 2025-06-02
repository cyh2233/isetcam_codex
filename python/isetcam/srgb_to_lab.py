# mypy: ignore-errors
"""Convert nonlinear sRGB values to CIE L*a*b*."""

from __future__ import annotations

import numpy as np

from .srgb_xyz import srgb_to_xyz
from .xyz_to_lab import xyz_to_lab


def srgb_to_lab(srgb: np.ndarray, whitepoint: np.ndarray) -> np.ndarray:
    """Convert sRGB values to L*a*b*.

    Parameters
    ----------
    srgb : np.ndarray
        sRGB values in either ``(n, 3)`` XW format or ``(rows, cols, 3)`` RGB
        format.
    whitepoint : array-like
        Reference white point as ``(Xn, Yn, Zn)``.

    Returns
    -------
    np.ndarray
        L*a*b* values in the same spatial format as ``srgb``.
    """
    xyz = srgb_to_xyz(srgb)
    return xyz_to_lab(xyz, whitepoint)
