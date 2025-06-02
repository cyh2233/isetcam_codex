# mypy: ignore-errors
"""Insert faulty pixels into an image."""

from __future__ import annotations

import numpy as np


def faulty_insert(list_: np.ndarray, img: np.ndarray, val: float | int = 0) -> np.ndarray:
    """Return ``img`` with specified pixels set to ``val``.

    Parameters
    ----------
    list_ : np.ndarray
        ``(N, 2)`` array of ``(x, y)`` positions for faulty pixels.
    img : np.ndarray
        Image array with shape ``(rows, cols, channels)`` or ``(rows, cols)``.
    val : float | int, optional
        Value assigned to the faulty pixels. Default is ``0``.

    Returns
    -------
    np.ndarray
        Copy of ``img`` with the faulty pixel locations set to ``val``.
    """
    if list_.ndim != 2 or list_.shape[1] != 2:
        raise ValueError("list_ must be (N, 2) array")

    out = np.array(img, copy=True)
    h, w = out.shape[:2]
    for x, y in list_.astype(int):
        if not (0 <= x < w and 0 <= y < h):
            raise ValueError("faulty pixel location out of bounds")
        if out.ndim == 2:
            out[y, x] = val
        else:
            out[y, x, ...] = val
    return out
