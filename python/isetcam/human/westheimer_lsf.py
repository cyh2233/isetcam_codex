# mypy: ignore-errors
"""Westheimer line spread function."""

from __future__ import annotations

import numpy as np

_DEF_X = np.arange(-300, 301)


def westheimer_lsf(x_sec: np.ndarray | None = None) -> tuple[np.ndarray, np.ndarray]:
    """Return Westheimer line spread function."""
    if x_sec is None:
        x_sec = _DEF_X.copy()
    else:
        x_sec = np.asarray(x_sec, dtype=float)

    x_min = x_sec / 60.0
    ls = 0.47 * np.exp(-3.3 * (x_min ** 2)) + 0.53 * np.exp(-0.93 * np.abs(x_min))
    ls = ls / ls.sum()
    return ls, x_sec
