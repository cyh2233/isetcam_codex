# mypy: ignore-errors
"""Poirson & Wandell spatial chromatic filters."""

from __future__ import annotations

import numpy as np


def _ie_hwhm2sd(hwhm: float, gdim: int = 2) -> float:
    if gdim == 1:
        return hwhm / (2 * np.sqrt(np.log(2)))
    elif gdim == 2:
        return hwhm / np.sqrt(2 * np.log(2))
    raise ValueError("gdim must be 1 or 2")


def _gauss(hwhm: float, support: int) -> np.ndarray:
    x = np.arange(support) - round(support / 2)
    sd = _ie_hwhm2sd(hwhm, 1)
    g = np.exp(-((x / (2 * sd)) ** 2))
    return g / g.sum()


def _gauss2(hwhm_y: float, support_y: int, hwhm_x: float, support_x: int) -> np.ndarray:
    x = np.arange(support_x) - round(support_x / 2)
    y = np.arange(support_y) - round(support_y / 2)
    X, Y = np.meshgrid(x, y)
    sd_x = _ie_hwhm2sd(hwhm_x)
    sd_y = _ie_hwhm2sd(hwhm_y)
    g = np.exp(-0.5 * ((X / sd_x) ** 2 + (Y / sd_y) ** 2))
    return g / g.sum()


def _sum_gauss(params: list[float], dimension: int) -> np.ndarray:
    width = int(round(params[0]))
    n_gauss = (len(params) - 1) // 2
    if dimension == 2:
        g = np.zeros((width, width), dtype=float)
    else:
        g = np.zeros(width, dtype=float)
    for i in range(n_gauss):
        h = params[2 * i + 1]
        w = params[2 * i + 2]
        if dimension == 2:
            g0 = _gauss2(h, width, h, width)
        else:
            g0 = _gauss(h, width)
        g += w * g0
    return g / g.sum()


def poirson_spatio_chromatic(
    samp_per_deg: float | None = None, dimension: int = 2
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Return Poirson & Wandell spatio-chromatic filters."""
    if samp_per_deg is None:
        samp_per_deg = 241.0

    x1 = [0.05, 0.9207, 0.225, 0.105, 7.0, -0.1080]
    x2 = [0.0685, 0.5310, 0.826, 0.33]
    x3 = [0.0920, 0.4877, 0.6451, 0.3711]

    for idx in (0, 2, 4):
        if idx < len(x1):
            x1[idx] *= samp_per_deg
    for idx in (0, 2):
        if idx < len(x2):
            x2[idx] *= samp_per_deg
    for idx in (0, 2):
        if idx < len(x3):
            x3[idx] *= samp_per_deg

    width = int(np.ceil(samp_per_deg / 2) * 2 - 1)

    lum = _sum_gauss([width, *x1], dimension)
    rg = _sum_gauss([width, *x2], dimension)
    by = _sum_gauss([width, *x3], dimension)

    lum = lum / lum.sum()
    rg = rg / rg.sum()
    by = by / by.sum()

    center = (width + 1) / 2
    positions = (np.arange(width) - center) / samp_per_deg

    return lum, rg, by, positions


__all__ = ["poirson_spatio_chromatic"]
