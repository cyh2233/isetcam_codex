# mypy: ignore-errors
"""Convert row/column indices to a rectangle."""

from __future__ import annotations

from typing import Sequence, Tuple

import numpy as np


def vc_locs_to_rect(locs: Sequence[np.ndarray] | np.ndarray) -> Tuple[int, int, int, int]:
    """Return ``(x, y, width, height)`` from index arrays.

    Parameters
    ----------
    locs : tuple of array-like or Nx2 array
        Row and column indices describing the region. If a tuple is provided it
        should be ``(rows, cols)`` as returned by :func:`vc_rect_to_locs`. An
        ``(N, 2)`` array of points is also accepted.

    Returns
    -------
    tuple of int
        ``(x, y, width, height)`` describing the bounding rectangle.
    """
    if isinstance(locs, (tuple, list)):
        if len(locs) != 2:
            raise ValueError("locs must be a tuple of (rows, cols)")
        rows = np.asarray(locs[0], dtype=int).reshape(-1)
        cols = np.asarray(locs[1], dtype=int).reshape(-1)
    else:
        arr = np.asarray(locs, dtype=int)
        if arr.ndim != 2 or arr.shape[1] != 2:
            raise ValueError("locs must be (rows, cols) or Nx2 array")
        rows = arr[:, 0]
        cols = arr[:, 1]

    if rows.size == 0 or cols.size == 0:
        raise ValueError("locs must contain at least one point")

    y0 = int(rows.min())
    x0 = int(cols.min())
    h = int(rows.max() - y0 + 1)
    w = int(cols.max() - x0 + 1)
    return (x0, y0, w, h)


__all__ = ["vc_locs_to_rect"]
