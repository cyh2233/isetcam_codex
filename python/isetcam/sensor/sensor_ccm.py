# mypy: ignore-errors
"""Compute a color correction matrix from a Macbeth chart image."""

from __future__ import annotations

import numpy as np
from scipy.io import loadmat

from ..data_path import data_path
from .sensor_class import Sensor


_DEF_CORNERS_MSG = (
    "corners must be an array with shape (4, 2) specifying the chart "
    "corner points as (col, row) starting from lower left and proceeding "
    "clockwise"
)


def _chart_rectangles(corners: np.ndarray, n_rows: int = 4, n_cols: int = 6) -> tuple[np.ndarray, np.ndarray]:
    """Return patch size and midpoints for a chart.

    Parameters
    ----------
    corners : np.ndarray
        Four corner points ``(col, row)`` starting with the lower left and
        proceeding clockwise.
    n_rows, n_cols : int
        Number of rows and columns in the chart. Defaults correspond to the
        Macbeth ColorChecker.
    """
    cp = np.asarray(corners, dtype=float).reshape(4, 2)
    chart_x = np.linalg.norm(cp[3] - cp[2])
    chart_y = np.linalg.norm(cp[3] - cp[0])
    patch_size = np.array([chart_y / n_rows, chart_x / n_cols])

    mlocs = np.zeros((2, n_rows * n_cols), dtype=float)
    idx = 0
    for rr in range(n_rows):
        row_frac = rr / n_rows
        row_pt = (1 - row_frac) * cp[3] + row_frac * cp[0]
        row_pt[1] += patch_size[0] / 2
        for cc in range(n_cols):
            col_frac = cc / n_cols
            col_pt = (1 - col_frac) * cp[3] + col_frac * cp[2]
            col_pt[0] += patch_size[1] / 2
            pt = col_pt + row_pt - cp[3]
            mlocs[:, idx] = pt[[1, 0]]
            idx += 1
    return patch_size, mlocs


def _patch_means(img: np.ndarray, centers: np.ndarray, delta: int) -> np.ndarray:
    """Return mean values around ``centers`` with square half-width ``delta``."""
    h, w = img.shape[:2]
    n = centers.shape[1]
    chans = 1 if img.ndim == 2 else img.shape[2]
    out = np.zeros((n, chans), dtype=float)
    for i in range(n):
        r = int(round(centers[0, i]))
        c = int(round(centers[1, i]))
        r0 = max(r - delta // 2, 0)
        c0 = max(c - delta // 2, 0)
        r1 = min(r0 + delta, h)
        c1 = min(c0 + delta, w)
        patch = img[r0:r1, c0:c1]
        out[i] = np.nanmean(patch.reshape(-1, chans), axis=0)
    return out


def _ideal_macbeth() -> np.ndarray:
    mat = loadmat(data_path("surfaces/charts/macbethChartLinearRGB.mat"))
    return mat["mcc"][0, 0]["lrgbValuesMCC"].astype(float)


def sensor_ccm(sensor: Sensor, corners: np.ndarray) -> np.ndarray:
    """Return a 3x3 CCM fitted from a Macbeth chart image."""
    if corners is None:
        raise ValueError("corner positions are required")
    cp = np.asarray(corners, dtype=float)
    if cp.shape != (4, 2):
        raise ValueError(_DEF_CORNERS_MSG)

    patch_size, centers = _chart_rectangles(cp)
    delta = int(round(patch_size[0] * 0.5))
    rgb = _patch_means(sensor.volts, centers, delta)

    ideal = _ideal_macbeth()
    if rgb.shape[0] != ideal.shape[0] or rgb.shape[1] != ideal.shape[1]:
        raise ValueError("sensor data must have 24 patches and 3 channels")

    L, _, _, _ = np.linalg.lstsq(rgb, ideal, rcond=None)
    return L


__all__ = ["sensor_ccm"]
