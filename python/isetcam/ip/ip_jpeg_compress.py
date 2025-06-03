# mypy: ignore-errors
"""JPEG-like DCT quantization of a grayscale image."""

from __future__ import annotations

import numpy as np
from scipy.fftpack import dct

__all__ = ["ip_jpeg_compress"]


def _jpeg_qtable(qfactor: float, table: int = 1) -> np.ndarray:
    qfactor = float(qfactor)
    if qfactor < 1:
        qfactor = 1
    if qfactor > 100:
        qfactor = 100
    if qfactor < 50:
        scale = 5000 / qfactor
    else:
        scale = 200 - 2 * qfactor

    if table == 1:
        q = np.array([
            [16, 11, 12, 14, 12, 10, 16, 14],
            [13, 14, 18, 17, 16, 19, 24, 40],
            [26, 24, 22, 22, 24, 49, 35, 37],
            [29, 40, 58, 51, 61, 60, 57, 51],
            [56, 55, 64, 72, 92, 78, 64, 68],
            [87, 69, 55, 56, 80, 109, 81, 87],
            [95, 98, 103, 104, 103, 62, 77, 113],
            [121, 112, 100, 120, 92, 101, 103, 99],
        ], dtype=float)
    elif table == 2:
        q = np.array([
            [17, 18, 18, 24, 21, 24, 47, 26],
            [26, 47, 99, 66, 56, 66, 99, 99],
            [99, 99, 99, 99, 99, 99, 99, 99],
            [99, 99, 99, 99, 99, 99, 99, 99],
            [99, 99, 99, 99, 99, 99, 99, 99],
            [99, 99, 99, 99, 99, 99, 99, 99],
            [99, 99, 99, 99, 99, 99, 99, 99],
            [99, 99, 99, 99, 99, 99, 99, 99],
        ], dtype=float)
    else:
        raise ValueError("table must be 1 or 2")

    q = np.floor((q * scale + 50) / 100)
    q = np.clip(q, 1, 255)
    return q


def _dct2(block: np.ndarray) -> np.ndarray:
    return dct(dct(block, axis=0, norm="ortho"), axis=1, norm="ortho")


def ip_jpeg_compress(im: np.ndarray, qinfo: float | np.ndarray = 50) -> np.ndarray:
    """Return quantized DCT coefficients of ``im``.

    Parameters
    ----------
    im : np.ndarray
        Grayscale image with values in range 0-255 or 0-1.
    qinfo : float or np.ndarray, optional
        Quality factor (1-100) or custom 8x8 quantization table.
        Defaults to ``50``.
    """
    im = np.asarray(im, dtype=float)
    if im.ndim != 2:
        raise ValueError("Image must be 2-D")

    if np.isscalar(qinfo):
        qtable = _jpeg_qtable(float(qinfo), 1)
    else:
        qtable = np.asarray(qinfo, dtype=float)
        if qtable.shape != (8, 8):
            raise ValueError("qinfo must be scalar or 8x8 table")

    if im.max() <= 1.0:
        im = im * 255.0

    r, c = im.shape
    r = (r // 8) * 8
    c = (c // 8) * 8
    im = im[:r, :c]

    coef = np.zeros_like(im)
    for i in range(0, r, 8):
        for j in range(0, c, 8):
            block = im[i : i + 8, j : j + 8]
            d = _dct2(block)
            coef[i : i + 8, j : j + 8] = np.round(d / qtable) * qtable
    return coef
