"""Apply :func:`ie_scale` to each column of an array."""

from __future__ import annotations

import numpy as np

from .ie_scale import ie_scale


def ie_scale_columns(X: np.ndarray, b1: float | None = 1.0, b2: float | None = None) -> np.ndarray:
    """Scale each column of ``X`` using :func:`ie_scale`.

    Parameters
    ----------
    X : np.ndarray
        Input matrix whose columns will be scaled.
    b1 : float, optional
        When ``b2`` is ``None`` this value becomes the maximum of each scaled
        column. Otherwise it is the lower bound of the output range.
    b2 : float, optional
        Upper bound of the output range for each column. When omitted, only a
        single bound ``b1`` is used and columns are scaled so their maxima equal
        ``b1``.

    Returns
    -------
    np.ndarray
        Matrix with each column individually scaled.
    """

    X = np.asarray(X, dtype=float)
    result = np.zeros_like(X)
    if b2 is None:
        for ii in range(X.shape[1]):
            result[:, ii], _, _ = ie_scale(X[:, ii], b1)
    else:
        for ii in range(X.shape[1]):
            result[:, ii], _, _ = ie_scale(X[:, ii], b1, b2)
    return result


__all__ = ["ie_scale_columns"]
