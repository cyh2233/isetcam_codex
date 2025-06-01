"""Percentile calculation compatible with MATLAB's ``prctile``."""

from __future__ import annotations

import numpy as np


def ie_prctile(x: np.ndarray, p: np.ndarray | float) -> np.ndarray:
    """Return percentiles of ``x``.

    Parameters
    ----------
    x : array-like
        Input data. For multi-dimensional arrays, percentiles are computed
        along the first axis (rows) matching MATLAB behavior.
    p : array-like or float
        Percentile or percentiles in the range [0, 100].

    Returns
    -------
    np.ndarray
        Percentile values. If ``p`` is a scalar the result is a row vector
        containing the percentile of each column of ``x``. When ``p`` is a
        vector, each row contains the corresponding percentile.
    """
    arr = np.asarray(x, dtype=float)
    perc = np.asarray(p, dtype=float).reshape(-1)

    if np.any(perc < 0) or np.any(perc > 100):
        raise ValueError("p must be between 0 and 100")

    if arr.ndim == 1:
        arr = arr.reshape(-1, 1)

    result = np.percentile(arr, perc, axis=0)
    return result


__all__ = ["ie_prctile"]
