# mypy: ignore-errors
"""Convert between sRGB and CIE XYZ color spaces."""

from __future__ import annotations

import numpy as np

from .rgb_to_xw_format import rgb_to_xw_format
from .xw_to_rgb_format import xw_to_rgb_format

# XYZ to linear RGB matrix (row-vector form) from the sRGB standard
_XYZ2LRGB = np.array([
    [3.2410, -0.9692, 0.0556],
    [-1.5374, 1.8760, -0.2040],
    [-0.4986, 0.0416, 1.0570],
])

# Inverse matrix for converting linear RGB to XYZ.
_LRGB2XYZ = np.linalg.inv(_XYZ2LRGB)


_DEF_LRGB_EPS = 0.0031308
_DEF_SRGB_EPS = 0.04045


def srgb_to_linear(srgb: np.ndarray) -> np.ndarray:
    """Convert nonlinear sRGB values to linear RGB.

    Parameters
    ----------
    srgb : np.ndarray
        sRGB values in ``[0, 1]``.

    Returns
    -------
    np.ndarray
        Linear RGB values in the same shape as ``srgb``.
    """
    srgb = np.asarray(srgb, dtype=float)
    lrgb = srgb.copy()
    mask = lrgb > _DEF_SRGB_EPS
    lrgb[mask] = ((lrgb[mask] + 0.055) / 1.055) ** 2.4
    lrgb[~mask] = lrgb[~mask] / 12.92
    return lrgb


def linear_to_srgb(lrgb: np.ndarray) -> np.ndarray:
    """Convert linear RGB values to nonlinear sRGB."""
    lrgb = np.asarray(lrgb, dtype=float)
    if lrgb.max() > 1 or lrgb.min() < 0:
        raise ValueError("Linear rgb values must be between 0 and 1")
    srgb = lrgb.copy()
    mask = srgb > _DEF_LRGB_EPS
    srgb[mask] = 1.055 * srgb[mask] ** (1 / 2.4) - 0.055
    srgb[~mask] = srgb[~mask] * 12.92
    return srgb


def srgb_to_xyz(srgb: np.ndarray) -> np.ndarray:
    """Convert sRGB image data to CIE XYZ.

    Parameters
    ----------
    srgb : np.ndarray
        RGB values in either ``(N, 3)`` XW format or ``(R, C, 3)`` RGB format.

    Returns
    -------
    np.ndarray
        XYZ values in the same spatial format as ``srgb``.
    """
    if srgb.ndim == 3:
        xw, r, c = rgb_to_xw_format(srgb)
        reshape = True
    elif srgb.ndim == 2 and srgb.shape[1] == 3:
        xw = srgb
        reshape = False
    else:
        raise ValueError("srgb must be (rows, cols, 3) or (n, 3)")

    lrgb = srgb_to_linear(xw)
    xyz = lrgb @ _LRGB2XYZ

    if reshape:
        xyz = xw_to_rgb_format(xyz, r, c)
    return xyz


def xyz_to_srgb(xyz: np.ndarray) -> tuple[np.ndarray, np.ndarray, float]:
    """Convert CIE XYZ values to sRGB.

    Parameters
    ----------
    xyz : np.ndarray
        XYZ values in either ``(N, 3)`` or ``(R, C, 3)`` format.

    Returns
    -------
    tuple[np.ndarray, np.ndarray, float]
        Tuple containing ``srgb`` values, the intermediate linear RGB
        ``lrgb`` array, and the normalization factor ``maxY`` applied to the
        input XYZ data.
    """
    if xyz.ndim == 3:
        xw, r, c = rgb_to_xw_format(xyz)
        reshape = True
    elif xyz.ndim == 2 and xyz.shape[1] == 3:
        xw = xyz
        reshape = False
    else:
        raise ValueError("xyz must be (rows, cols, 3) or (n, 3)")

    Y = xw[:, 1]
    maxY = float(Y.max())
    if maxY > 1:
        xw = xw / maxY
    else:
        maxY = 1.0

    if xw.min() < 0:
        xw = np.clip(xw, 0.0, 1.0)

    lrgb = xw @ _XYZ2LRGB
    srgb = linear_to_srgb(np.clip(lrgb, 0.0, 1.0))

    if reshape:
        srgb = xw_to_rgb_format(srgb, r, c)
        lrgb = xw_to_rgb_format(lrgb, r, c)
    return srgb, lrgb, maxY
