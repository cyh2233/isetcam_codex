# mypy: ignore-errors
"""Conversions between RGB and YCbCr color spaces."""

from __future__ import annotations

import numpy as np

from .color_transform_matrix import color_transform_matrix
from .rgb_to_xw_format import rgb_to_xw_format
from .xw_to_rgb_format import xw_to_rgb_format


def rgb_to_ycbcr(rgb: np.ndarray) -> np.ndarray:
    """Convert RGB values to YCbCr.

    Parameters
    ----------
    rgb : np.ndarray
        RGB values in either ``(n, 3)`` XW format or ``(rows, cols, 3)`` RGB
        format.

    Returns
    -------
    np.ndarray
        YCbCr values in the same spatial format as ``rgb``.
    """
    rgb = np.asarray(rgb, dtype=float)

    if rgb.ndim == 3:
        xw, r, c = rgb_to_xw_format(rgb)
        reshape = True
    elif rgb.ndim == 2 and rgb.shape[1] == 3:
        xw = rgb
        reshape = False
    else:
        raise ValueError("rgb must be (rows, cols, 3) or (n, 3)")

    T = color_transform_matrix('rgb2yuv')
    ycbcr = xw @ T

    if reshape:
        ycbcr = xw_to_rgb_format(ycbcr, r, c)

    return ycbcr


def ycbcr_to_rgb(ycbcr: np.ndarray) -> np.ndarray:
    """Convert YCbCr values to RGB.

    Parameters
    ----------
    ycbcr : np.ndarray
        YCbCr values in either ``(n, 3)`` XW format or ``(rows, cols, 3)`` RGB
        format.

    Returns
    -------
    np.ndarray
        RGB values in the same spatial format as ``ycbcr``.
    """
    ycbcr = np.asarray(ycbcr, dtype=float)

    if ycbcr.ndim == 3:
        xw, r, c = rgb_to_xw_format(ycbcr)
        reshape = True
    elif ycbcr.ndim == 2 and ycbcr.shape[1] == 3:
        xw = ycbcr
        reshape = False
    else:
        raise ValueError("ycbcr must be (rows, cols, 3) or (n, 3)")

    T = color_transform_matrix('yuv2rgb')
    rgb = xw @ T

    if reshape:
        rgb = xw_to_rgb_format(rgb, r, c)

    return rgb
