# mypy: ignore-errors
"""POCS demosaicing algorithm."""

from __future__ import annotations

import numpy as np
from scipy.signal import convolve2d

from .ie_bilinear import ie_bilinear


def _bayer_masks(pattern: str, rows: int, cols: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    pattern = pattern.lower()
    if pattern not in {"rggb", "bggr", "gbrg", "grbg"}:
        raise ValueError("Unsupported CFA pattern")
    grid = np.array([[pattern[0], pattern[1]], [pattern[2], pattern[3]]])
    r = np.zeros((rows, cols), bool)
    g = np.zeros((rows, cols), bool)
    b = np.zeros((rows, cols), bool)
    for i in range(rows):
        for j in range(cols):
            ch = grid[i % 2, j % 2]
            if ch == "r":
                r[i, j] = True
            elif ch == "g":
                g[i, j] = True
            else:
                b[i, j] = True
    return r, g, b


def _rdwt2(x: np.ndarray, h0: np.ndarray, h1: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    height, width = x.shape
    t0 = int(np.ceil(len(h0) / 2))

    z = convolve2d(x, h0[np.newaxis, :], mode="full")
    a = convolve2d(z, h0[:, np.newaxis], mode="full")
    a = a[t0 : t0 + height, t0 : t0 + width]
    h = convolve2d(z, h1[:, np.newaxis], mode="full")
    h = h[t0 : t0 + height, t0 : t0 + width]

    z = convolve2d(x, h1[np.newaxis, :], mode="full")
    v = convolve2d(z, h0[:, np.newaxis], mode="full")
    v = v[t0 : t0 + height, t0 : t0 + width]
    d = convolve2d(z, h1[:, np.newaxis], mode="full")
    d = d[t0 : t0 + height, t0 : t0 + width]

    return a, h, v, d


def _ridwt2(a: np.ndarray, h: np.ndarray, v: np.ndarray, d: np.ndarray, g0: np.ndarray, g1: np.ndarray) -> np.ndarray:
    height, width = a.shape
    t0 = int(np.ceil(len(g0) / 2))
    kernel_a = np.outer(g0, g0)
    kernel_h = np.outer(g1, g0)
    kernel_v = np.outer(g0, g1)
    kernel_d = np.outer(g1, g1)
    x = (
        convolve2d(a, kernel_a, mode="full")
        + convolve2d(h, kernel_h, mode="full")
        + convolve2d(v, kernel_v, mode="full")
        + convolve2d(d, kernel_d, mode="full")
    )
    return x[t0 : t0 + height, t0 : t0 + width]


def pocs(bayer: np.ndarray, pattern: str, iter_n: int = 20) -> np.ndarray:
    """Demosaic ``bayer`` using Projection Onto Convex Sets."""

    bayer = np.asarray(bayer, dtype=float)
    if bayer.ndim != 2:
        raise ValueError("bayer must be a 2-D array")

    rows, cols = bayer.shape
    r_mask, g_mask, b_mask = _bayer_masks(pattern, rows, cols)

    rgb = ie_bilinear(bayer, pattern).astype(float)
    r = rgb[:, :, 0]
    g = rgb[:, :, 1]
    b = rgb[:, :, 2]

    h0 = np.array([1, 2, 1], dtype=float) / 4
    h1 = np.array([1, -2, 1], dtype=float) / 4
    g0 = np.array([-1, 2, 6, 2, -1], dtype=float) / 8
    g1 = np.array([1, 2, -6, 2, 1], dtype=float) / 8

    for _ in range(iter_n):
        ca_r, ch_r, cv_r, cd_r = _rdwt2(r, h0, h1)
        ca_g, ch_g, cv_g, cd_g = _rdwt2(g, h0, h1)
        ca_b, ch_b, cv_b, cd_b = _rdwt2(b, h0, h1)

        r_new = _ridwt2(ca_r, ch_g, cv_g, cd_g, g0, g1)
        g_new = _ridwt2(ca_g, ch_g, cv_g, cd_g, g0, g1)
        b_new = _ridwt2(ca_b, ch_g, cv_g, cd_g, g0, g1)

        r_new[r_mask] = bayer[r_mask]
        b_new[b_mask] = bayer[b_mask]

        r, g, b = r_new, g_new, b_new

    out = np.stack([r, g, b], axis=2)
    return out

__all__ = ["pocs"]
