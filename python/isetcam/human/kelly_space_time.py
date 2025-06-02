# mypy: ignore-errors
"""Kelly 1979 spatio-temporal sensitivity model."""

from __future__ import annotations

import numpy as np

_DEF_FS = 10 ** np.arange(-0.5, 1.3 + 0.05, 0.05)
_DEF_FT = 10 ** np.arange(-0.5, 1.7 + 0.05, 0.05)


def kelly_space_time(
    fs: np.ndarray | None = None,
    ft: np.ndarray | None = None,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return Kelly's space-time sensitivity surface."""
    if fs is None:
        fs = _DEF_FS.copy()
    else:
        fs = np.asarray(fs, dtype=float)
    if ft is None:
        ft = _DEF_FT.copy()
    else:
        ft = np.asarray(ft, dtype=float)

    ft_grid, fs_grid = np.meshgrid(ft, fs)

    alpha = 2 * np.pi * fs_grid
    v = ft_grid / fs_grid
    k = 6.1 + 7.3 * (np.abs(np.log10(v / 3))) ** 3
    amax = 45.9 / (v + 2)
    sens = k * v * (alpha ** 2) * np.exp(-2 * alpha / amax)

    sens[sens < 1] = np.nan
    sens = sens / 2

    return sens, fs, ft
