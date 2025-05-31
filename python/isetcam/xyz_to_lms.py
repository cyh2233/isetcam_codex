"""Convert CIE XYZ values to Stockman LMS cone responses.

This function optionally simulates various forms of color blindness
according to the Brettel, Vienot and Mollon model.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import numpy as np
from scipy.io import loadmat

from .rgb_to_xw_format import rgb_to_xw_format
from .xw_to_rgb_format import xw_to_rgb_format
from .data_path import data_path

# XYZ to LMS conversion matrix (Stockman fundamentals)
_XYZ2LMS = np.array([
    [0.2689, 0.8518, -0.0358],
    [-0.3962, 1.1770, 0.1055],
    [0.0214, -0.0247, 0.5404],
])


_def_stockman_path = data_path("human/stockman.mat")


def _stockman_values(wavelengths: list[float]) -> np.ndarray:
    """Return Stockman LMS values at the requested wavelengths."""
    data = loadmat(_def_stockman_path)
    wave = data["wavelength"].ravel()
    vals = data["data"]
    result = np.zeros((len(wavelengths), 3))
    for i in range(3):
        result[:, i] = np.interp(wavelengths, wave, vals[:, i])
    return result


_def_anchor_wavelengths = [475, 485, 575, 660]


def xyz_to_lms(
    xyz: np.ndarray,
    cb_type: int = 0,
    white_xyz: Optional[np.ndarray] = None,
    extrap_val: float = 0.0,
) -> np.ndarray:
    """Convert XYZ values to LMS.

    Parameters
    ----------
    xyz : np.ndarray
        XYZ values in either ``(n, 3)`` XW format or ``(rows, cols, 3)`` RGB
        format.
    cb_type : int, optional
        Color blindness simulation type. ``1`` = protanopia, ``2`` =
        deuteranopia, ``3`` = tritanopia. Negative values set the corresponding
        cone class to ``extrap_val``. Default ``0`` (no simulation).
    white_xyz : array-like, optional
        Reference white point required when ``cb_type`` is positive.
    extrap_val : float, optional
        Value to place in the missing cone class when ``cb_type`` is
        negative. Ignored otherwise.

    Returns
    -------
    np.ndarray
        LMS values in the same spatial format as ``xyz``.
    """
    xyz = np.asarray(xyz, dtype=float)

    if xyz.ndim == 3:
        xw, r, c = rgb_to_xw_format(xyz)
        reshape = True
    elif xyz.ndim == 2 and xyz.shape[1] == 3:
        xw = xyz
        reshape = False
    else:
        raise ValueError("xyz must be (rows, cols, 3) or (n, 3)")

    lms = xw @ _XYZ2LMS

    if cb_type > 0:
        if white_xyz is None:
            raise ValueError("white_xyz required when cb_type > 0")
        anchor_e = np.asarray(white_xyz, dtype=float).reshape(1, 3) @ _XYZ2LMS
        anchor_vals = _stockman_values(_def_anchor_wavelengths)
        a1 = a2 = b1 = b2 = c1 = c2 = None
        if cb_type == 1:  # protanopia
            a1 = anchor_e[0, 1] * anchor_vals[2, 2] - anchor_e[0, 2] * anchor_vals[2, 1]
            b1 = anchor_e[0, 2] * anchor_vals[2, 0] - anchor_e[0, 0] * anchor_vals[2, 2]
            c1 = anchor_e[0, 0] * anchor_vals[2, 1] - anchor_e[0, 1] * anchor_vals[2, 0]
            a2 = anchor_e[0, 1] * anchor_vals[0, 2] - anchor_e[0, 2] * anchor_vals[0, 1]
            b2 = anchor_e[0, 2] * anchor_vals[0, 0] - anchor_e[0, 0] * anchor_vals[0, 2]
            c2 = anchor_e[0, 0] * anchor_vals[0, 1] - anchor_e[0, 1] * anchor_vals[0, 0]
            inflection = anchor_e[0, 2] / anchor_e[0, 1]
            L, M, S = lms[:, 0], lms[:, 1], lms[:, 2]
            ratio = np.divide(S, M, out=np.full_like(S, np.inf), where=M != 0)
            mask = ratio < inflection
            L[mask] = -(b1 * M[mask] + c1 * S[mask]) / a1
            L[~mask] = -(b2 * M[~mask] + c2 * S[~mask]) / a2
            lms[:, 0] = L
        elif cb_type == 2:  # deuteranopia
            a1 = anchor_e[0, 1] * anchor_vals[2, 2] - anchor_e[0, 2] * anchor_vals[2, 1]
            b1 = anchor_e[0, 2] * anchor_vals[2, 0] - anchor_e[0, 0] * anchor_vals[2, 2]
            c1 = anchor_e[0, 0] * anchor_vals[2, 1] - anchor_e[0, 1] * anchor_vals[2, 0]
            a2 = anchor_e[0, 1] * anchor_vals[0, 2] - anchor_e[0, 2] * anchor_vals[0, 1]
            b2 = anchor_e[0, 2] * anchor_vals[0, 0] - anchor_e[0, 0] * anchor_vals[0, 2]
            c2 = anchor_e[0, 0] * anchor_vals[0, 1] - anchor_e[0, 1] * anchor_vals[0, 0]
            inflection = anchor_e[0, 2] / anchor_e[0, 0]
            L, M, S = lms[:, 0], lms[:, 1], lms[:, 2]
            ratio = np.divide(S, L, out=np.full_like(S, np.inf), where=L != 0)
            mask = ratio < inflection
            M[mask] = -(a1 * L[mask] + c1 * S[mask]) / b1
            M[~mask] = -(a2 * L[~mask] + c2 * S[~mask]) / b2
            lms[:, 1] = M
        elif cb_type == 3:  # tritanopia
            a1 = anchor_e[0, 1] * anchor_vals[3, 2] - anchor_e[0, 2] * anchor_vals[3, 1]
            b1 = anchor_e[0, 2] * anchor_vals[3, 0] - anchor_e[0, 0] * anchor_vals[3, 2]
            c1 = anchor_e[0, 0] * anchor_vals[3, 1] - anchor_e[0, 1] * anchor_vals[3, 0]
            a2 = anchor_e[0, 1] * anchor_vals[1, 2] - anchor_e[0, 2] * anchor_vals[1, 1]
            b2 = anchor_e[0, 2] * anchor_vals[1, 0] - anchor_e[0, 0] * anchor_vals[1, 2]
            c2 = anchor_e[0, 0] * anchor_vals[1, 1] - anchor_e[0, 1] * anchor_vals[1, 0]
            inflection = anchor_e[0, 1] / anchor_e[0, 0]
            L, M, S = lms[:, 0], lms[:, 1], lms[:, 2]
            ratio = np.divide(M, L, out=np.full_like(M, np.inf), where=L != 0)
            mask = ratio < inflection
            S[mask] = -(a1 * L[mask] + b1 * M[mask]) / c1
            S[~mask] = -(a2 * L[~mask] + b2 * M[~mask]) / c2
            lms[:, 2] = S
    elif cb_type < 0:
        cone = -cb_type
        if cone == 1:
            lms[:, 0] = extrap_val
        elif cone == 2:
            lms[:, 1] = extrap_val
        elif cone == 3:
            lms[:, 2] = extrap_val

    if reshape:
        lms = xw_to_rgb_format(lms, r, c)

    return lms
