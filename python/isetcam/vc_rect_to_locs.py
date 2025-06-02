# mypy: ignore-errors
"""Convert a rectangle ROI to row/column index arrays."""

from __future__ import annotations

from typing import Sequence, Tuple

import numpy as np


def vc_rect_to_locs(rect: Sequence[int]) -> Tuple[np.ndarray, np.ndarray]:
    """Return index arrays corresponding to ``rect``.

    Parameters
    ----------
    rect : sequence of int
        Rectangle given as ``(x, y, width, height)`` using 0-based indexing.

    Returns
    -------
    tuple of np.ndarray
        ``(rows, cols)`` arrays selecting the rectangle.
    """
    if len(rect) != 4:
        raise ValueError("rect must have four elements (x, y, width, height)")

    x, y, w, h = [int(v) for v in rect]
    if w <= 0 or h <= 0:
        raise ValueError("width and height must be positive")

    rows = np.arange(y, y + h, dtype=int)
    cols = np.arange(x, x + w, dtype=int)
    return rows, cols


__all__ = ["vc_rect_to_locs"]
