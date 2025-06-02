# mypy: ignore-errors
from __future__ import annotations

import numpy as np
from scipy.ndimage import convolve1d


def _centroid(v: np.ndarray, w: np.ndarray) -> float:
    return float(np.sum(np.arange(v.size) * v * w) / np.sum(v * w))


def iso12233_sfr(
    bar_image: np.ndarray,
    delta_x: float = 0.002,
    weight: tuple[float, float, float] = (0.213, 0.715, 0.072),
) -> tuple[np.ndarray, np.ndarray]:
    """Return spatial frequency response of a slanted-edge ``bar_image``.

    Parameters
    ----------
    bar_image : np.ndarray
        2-D or 3-D array containing a slanted edge.
    delta_x : float, optional
        Sample spacing in millimeters. ``1`` interprets units as pixels.
    weight : tuple of float, optional
        RGB weights used when ``bar_image`` is color.

    Returns
    -------
    np.ndarray
        Spatial frequencies in cycles/mm.
    np.ndarray
        Modulation transfer function values.
    """
    img = np.asarray(bar_image, dtype=float)
    if img.ndim == 3:
        if img.shape[2] != 3:
            raise ValueError("bar_image must have 3 channels when 3-D")
        w = np.asarray(weight, dtype=float).reshape(3)
        img = img @ w

    # Rotate to vertical edge if needed
    if np.sum(np.abs(np.diff(img, axis=0))) > np.sum(np.abs(np.diff(img, axis=1))):
        img = img.T
    n_row, n_col = img.shape

    fil1 = np.array([0.5, -0.5])
    fil2 = np.array([0.5, 0.0, -0.5])
    if np.sum(img[:, :5]) > np.sum(img[:, -5:]):
        fil1 = -fil1
        fil2 = -fil2

    lsf_rows = convolve1d(img, fil1, axis=1, mode="nearest")
    window1 = np.hamming(n_col)
    loc = np.array([_centroid(r, window1) - 0.5 for r in lsf_rows])
    p = np.polyfit(np.arange(n_row), loc, 1)
    loc2 = np.empty_like(loc)
    for y in range(n_row):
        loc2[y] = _centroid(lsf_rows[y], window1) - 0.5
    p = np.polyfit(np.arange(n_row), loc2, 1)
    slope, intercept = p

    nbin = 4
    nn = int(np.floor(n_col * nbin))
    accum = np.zeros(nn)
    counts = np.zeros(nn)
    x = np.arange(n_col)
    for y in range(n_row):
        x0 = slope * y + intercept
        idx = np.round((x - x0) * nbin).astype(int)
        m = (0 <= idx) & (idx < nn)
        b = idx[m]
        np.add.at(accum, b, img[y, m])
        np.add.at(counts, b, 1)
    point = np.zeros(nn)
    for i in range(nn):
        if counts[i] > 0:
            point[i] = accum[i] / counts[i]
        else:
            if i == 0 and counts[i + 1] > 0:
                point[i] = accum[i + 1] / counts[i + 1]
            elif i == nn - 1 and counts[i - 1] > 0:
                point[i] = accum[i - 1] / counts[i - 1]
            elif 0 < i < nn - 1 and counts[i - 1] > 0 and counts[i + 1] > 0:
                point[i] = 0.5 * (
                    accum[i - 1] / counts[i - 1] + accum[i + 1] / counts[i + 1]
                )

    lsf = convolve1d(point, fil2, mode="nearest")
    win = np.hamming(nn)
    lsf *= win
    temp = np.abs(np.fft.fft(lsf))
    nn2 = nn // 2 + 1
    mtf = temp[:nn2] / temp[0]
    freq = nbin * np.arange(nn2) / (delta_x * nn)
    return freq, mtf


__all__ = ["iso12233_sfr"]
