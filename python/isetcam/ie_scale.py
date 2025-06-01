"""Scale numeric data to a specified range."""

from __future__ import annotations

import numpy as np
from typing import Tuple


def ie_scale(im: np.ndarray, b1: float | None = None, b2: float | None = None) -> Tuple[np.ndarray, float, float]:
    """Scale ``im`` into the range ``[b1, b2]``.

    The function mirrors the behavior of the MATLAB ``ieScale`` utility.

    Parameters
    ----------
    im : np.ndarray
        Input data to be scaled.
    b1 : float, optional
        Lower bound of the output range when ``b2`` is provided or the desired
        maximum value when ``b2`` is ``None``.
    b2 : float, optional
        Upper bound of the output range. When omitted, ``b1`` specifies the
        maximum value and the data are simply scaled so that the maximum equals
        ``b1``.

    Returns
    -------
    tuple[np.ndarray, float, float]
        The scaled array along with the minimum and maximum of the input data.
    """

    arr = np.asarray(im, dtype=float)
    mx = float(arr.max())
    mn = float(arr.min())

    if b1 is not None and b2 is None:
        # Single bound: scale so the maximum equals ``b1``
        if mx == 0:
            scaled = np.zeros_like(arr)
        else:
            scaled = arr * (float(b1) / mx)
        return scaled, mn, mx

    # Scale to [0, 1]
    if mx == mn:
        norm = np.zeros_like(arr)
    else:
        norm = (arr - mn) / (mx - mn)

    if b1 is None and b2 is None:
        b1, b2 = 0.0, 1.0
    elif b2 is not None:
        if b1 is None or b1 >= b2:
            raise ValueError("ie_scale: bad bounds values")
    else:
        # Should not reach here (handled by first branch)
        b1, b2 = 0.0, 1.0

    range_ = float(b2 - b1)
    scaled = range_ * norm + float(b1)
    return scaled, mn, mx


__all__ = ["ie_scale"]
