"""Nearest neighbor demosaicing for Bayer-pattern images."""

from __future__ import annotations

import numpy as np


def ie_nearest_neighbor(bayer: np.ndarray, pattern: str) -> np.ndarray:
    """Demosaic ``bayer`` using nearest neighbor interpolation.

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

    rows, cols = bayer.shape
    pattern = pattern.lower()
    if pattern not in {"rggb", "bggr", "grbg", "gbrg"}:
        raise ValueError("Unsupported CFA pattern")

    grid = np.array([[pattern[0], pattern[1]], [pattern[2], pattern[3]]])
    positions: dict[str, tuple[int, int]] = {}
    first_g = True
    for r in range(2):
        for c in range(2):
            ch = grid[r, c]
            if ch == "g":
                key = "g1" if first_g else "g2"
                positions[key] = (r, c)
                first_g = False
            else:
                positions[ch] = (r, c)

    r_pos = positions["r"]
    b_pos = positions["b"]
    g1_pos = positions["g1"]
    g2_pos = positions["g2"]

    rgb = np.zeros((rows, cols, 3), dtype=bayer.dtype)

    def _replicate_rb(pos: tuple[int, int], ch: int) -> None:
        dx = 1 if pos[1] == 0 else -1
        dy = 1 if pos[0] == 0 else -1
        for i in range(pos[0], rows, 2):
            for j in range(pos[1], cols, 2):
                val = bayer[i, j]
                rgb[i, j, ch] = val
                if 0 <= j + dx < cols:
                    rgb[i, j + dx, ch] = val
                if 0 <= i + dy < rows:
                    rgb[i + dy, j, ch] = val
                if 0 <= j + dx < cols and 0 <= i + dy < rows:
                    rgb[i + dy, j + dx, ch] = val

    _replicate_rb(r_pos, 0)
    _replicate_rb(b_pos, 2)

    g1_dx = -1 if g1_pos[1] == 1 else 1
    for i in range(g1_pos[0], rows, 2):
        for j in range(g1_pos[1], cols, 2):
            val = bayer[i, j]
            rgb[i, j, 1] = val
            jj = j + g1_dx
            if 0 <= jj < cols:
                rgb[i, jj, 1] = val
    for i in range(g2_pos[0], rows, 2):
        for j in range(g2_pos[1], cols, 2):
            val = bayer[i, j]
            rgb[i, j, 1] = val
            jj = j - g1_dx
            if 0 <= jj < cols:
                rgb[i, jj, 1] = val

    return rgb
