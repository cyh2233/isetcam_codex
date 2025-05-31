"""Repair faulty pixels in a Bayer mosaic."""

from __future__ import annotations

import numpy as np


def faulty_pixel_correction(
    list_: np.ndarray,
    bayer: np.ndarray,
    pattern: str,
    method: str = "bilinear",
) -> np.ndarray:
    """Return ``bayer`` with faulty pixels replaced.

    Parameters
    ----------
    list_ : np.ndarray
        ``(N, 2)`` array with faulty pixel ``(x, y)`` coordinates.
    bayer : np.ndarray
        2-D Bayer mosaic image.
    pattern : str
        CFA pattern string such as ``"rggb"``.
    method : {{"bilinear", "nearest"}}, optional
        Interpolation method. Default is ``"bilinear"``.

    Returns
    -------
    np.ndarray
        Corrected Bayer mosaic.
    """
    if list_.ndim != 2 or list_.shape[1] != 2:
        raise ValueError("list_ must be (N, 2) array")
    if bayer.ndim != 2:
        raise ValueError("bayer must be a 2-D array")

    pattern = pattern.lower()
    if pattern not in {"rggb", "bggr", "grbg", "gbrg"}:
        raise ValueError("Unsupported CFA pattern")

    grid = np.array([[pattern[0], pattern[1]], [pattern[2], pattern[3]]])

    bayer = np.array(bayer, dtype=float)
    out = bayer.copy()

    pad = 2 if method == "bilinear" else 2
    padded = np.pad(bayer, pad, mode="edge")

    for x, y in list_.astype(int):
        if not (0 <= y < bayer.shape[0] and 0 <= x < bayer.shape[1]):
            raise ValueError("faulty pixel location out of bounds")
        color = grid[y % 2, x % 2]
        yp = y + pad
        xp = x + pad
        if method == "nearest":
            if color in {"r", "b"}:
                val = padded[yp + 2, xp]
            else:
                val = padded[yp + 1, xp + 1]
        else:  # bilinear
            if color in {"r", "b"}:
                vals = [
                    padded[yp - 2, xp],
                    padded[yp + 2, xp],
                    padded[yp, xp - 2],
                    padded[yp, xp + 2],
                ]
            else:  # green
                vals = [
                    padded[yp - 1, xp - 1],
                    padded[yp - 1, xp + 1],
                    padded[yp + 1, xp - 1],
                    padded[yp + 1, xp + 1],
                ]
            val = sum(vals) / 4.0
        out[y, x] = val

    return out
