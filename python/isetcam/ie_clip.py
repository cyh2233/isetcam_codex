"""Clip values to a specified range."""

from __future__ import annotations

import numpy as np
from typing import Any


_SENTINEL = object()


def ie_clip(data: np.ndarray, lower: Any = _SENTINEL, upper: Any = _SENTINEL) -> np.ndarray:
    """Clip ``data`` to the provided bounds.

    Parameters
    ----------
    data : np.ndarray
        Array of values to be clipped.
    lower : float or None, optional
        Lower clipping bound. When not provided and ``upper`` is also not
        provided, the default range ``[0, 1]`` is used. If a single numeric
        bound is provided (``lower`` or ``upper``), the data are clipped
        symmetrically to ``[-abs(b), abs(b)]``. ``None`` disables the lower
        bound.
    upper : float or None, optional
        Upper clipping bound. ``None`` disables the upper bound.

    Returns
    -------
    np.ndarray
        The clipped array.
    """
    arr = np.asarray(data)

    # Determine clipping bounds following MATLAB semantics
    if lower is _SENTINEL and upper is _SENTINEL:
        lower, upper = 0.0, 1.0
    elif lower is not _SENTINEL and upper is _SENTINEL:
        if lower is None:
            return arr
        bound = float(abs(lower))
        lower, upper = -bound, bound
    elif lower is _SENTINEL and upper is not _SENTINEL:
        if upper is None:
            return arr
        bound = float(abs(upper))
        lower, upper = -bound, bound

    # Both bounds provided (may include None)
    if lower is not None:
        arr = np.maximum(arr, float(lower))
    if upper is not None:
        arr = np.minimum(arr, float(upper))
    return arr
