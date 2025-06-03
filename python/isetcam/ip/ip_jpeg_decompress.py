# mypy: ignore-errors
"""Inverse DCT decoding of JPEG coefficients."""

from __future__ import annotations

import numpy as np
from scipy.fftpack import idct

__all__ = ["ip_jpeg_decompress"]


def _idct2(block: np.ndarray) -> np.ndarray:
    return idct(idct(block, axis=0, norm="ortho"), axis=1, norm="ortho")


def ip_jpeg_decompress(coef: np.ndarray) -> np.ndarray:
    """Return reconstructed image from quantized DCT coefficients."""
    coef = np.asarray(coef, dtype=float)
    if coef.ndim != 2:
        raise ValueError("Coefficients must be 2-D")
    r, c = coef.shape
    if r % 8 != 0 or c % 8 != 0:
        raise ValueError("Coefficient array size must be multiple of 8")

    img = np.zeros_like(coef)
    for i in range(0, r, 8):
        for j in range(0, c, 8):
            block = coef[i : i + 8, j : j + 8]
            img[i : i + 8, j : j + 8] = _idct2(block)
    return img
