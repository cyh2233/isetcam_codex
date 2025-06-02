# mypy: ignore-errors
"""Bilinear demosaicing for Bayer-pattern images."""

from __future__ import annotations

import numpy as np


def ie_bilinear(bayer: np.ndarray, pattern: str) -> np.ndarray:
    """Demosaic ``bayer`` using simple bilinear interpolation.

    Parameters
    ----------
    bayer : np.ndarray
        2-D array containing the raw mosaic image.
    pattern : str
        CFA pattern string such as ``"rggb"``.

    Returns
    -------
    np.ndarray
        RGB image with shape ``(rows, cols, 3)``.
    """
    bayer = np.asarray(bayer)
    if bayer.ndim != 2:
        raise ValueError("bayer must be a 2-D array")

    dtype = bayer.dtype
    bayer = bayer.astype(float)
    rows, cols = bayer.shape

    pattern = pattern.lower()
    if pattern not in {"rggb", "bggr", "grbg", "gbrg"}:
        raise ValueError("Unsupported CFA pattern")

    grid = np.array([[pattern[0], pattern[1]], [pattern[2], pattern[3]]])

    r = np.zeros((rows, cols), float)
    g = np.zeros((rows, cols), float)
    b = np.zeros((rows, cols), float)

    for i in range(rows):
        for j in range(cols):
            ch = grid[i % 2, j % 2]
            if ch == "r":
                r[i, j] = bayer[i, j]
            elif ch == "g":
                g[i, j] = bayer[i, j]
            else:
                b[i, j] = bayer[i, j]

    r_pos = b_pos = (0, 0)
    for rr in range(2):
        for cc in range(2):
            ch = grid[rr, cc]
            if ch == "r":
                r_pos = (rr, cc)
            if ch == "b":
                b_pos = (rr, cc)

    g_new = g.copy()
    for i in range(rows):
        for j in range(cols):
            if grid[i % 2, j % 2] != "g":
                total = 0.0
                count = 0
                for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    ii, jj = i + di, j + dj
                    if 0 <= ii < rows and 0 <= jj < cols and g[ii, jj] != 0:
                        total += g[ii, jj]
                        count += 1
                if count > 0:
                    g_new[i, j] = total / count
    g = g_new

    r_new = r.copy()
    for i in range(rows):
        for j in range(cols):
            if grid[i % 2, j % 2] == "r":
                continue
            if grid[i % 2, j % 2] == "g":
                if i % 2 == r_pos[0]:
                    vals = [
                        r[i, j - 1] if j - 1 >= 0 else None,
                        r[i, j + 1] if j + 1 < cols else None,
                    ]
                else:
                    vals = [
                        r[i - 1, j] if i - 1 >= 0 else None,
                        r[i + 1, j] if i + 1 < rows else None,
                    ]
            else:  # blue location
                vals = [
                    r[i - 1, j - 1] if i - 1 >= 0 and j - 1 >= 0 else None,
                    r[i - 1, j + 1] if i - 1 >= 0 and j + 1 < cols else None,
                    r[i + 1, j - 1] if i + 1 < rows and j - 1 >= 0 else None,
                    r[i + 1, j + 1] if i + 1 < rows and j + 1 < cols else None,
                ]
            vals = [v for v in vals if v is not None]
            if vals:
                r_new[i, j] = sum(vals) / len(vals)
    r = r_new

    b_new = b.copy()
    for i in range(rows):
        for j in range(cols):
            if grid[i % 2, j % 2] == "b":
                continue
            if grid[i % 2, j % 2] == "g":
                if i % 2 == b_pos[0]:
                    vals = [
                        b[i, j - 1] if j - 1 >= 0 else None,
                        b[i, j + 1] if j + 1 < cols else None,
                    ]
                else:
                    vals = [
                        b[i - 1, j] if i - 1 >= 0 else None,
                        b[i + 1, j] if i + 1 < rows else None,
                    ]
            else:  # red location
                vals = [
                    b[i - 1, j - 1] if i - 1 >= 0 and j - 1 >= 0 else None,
                    b[i - 1, j + 1] if i - 1 >= 0 and j + 1 < cols else None,
                    b[i + 1, j - 1] if i + 1 < rows and j - 1 >= 0 else None,
                    b[i + 1, j + 1] if i + 1 < rows and j + 1 < cols else None,
                ]
            vals = [v for v in vals if v is not None]
            if vals:
                b_new[i, j] = sum(vals) / len(vals)
    b = b_new

    rgb = np.stack([r, g, b], axis=2)
    if np.issubdtype(dtype, np.integer):
        rgb = np.rint(rgb).astype(dtype)
    return rgb
