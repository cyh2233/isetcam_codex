# mypy: ignore-errors
"""Translate an image array."""

from __future__ import annotations

import numpy as np


def image_translate(img: np.ndarray, dx: int, dy: int, fill: float = 0) -> np.ndarray:
    """Shift ``img`` by ``dx`` and ``dy`` pixels.

    Parameters
    ----------
    img : np.ndarray
        Image data array. Can be 2-D or 3-D.
    dx, dy : int
        Horizontal and vertical shift in pixels. Positive values shift the
        image right and down respectively.
    fill : float, optional
        Fill value for areas exposed by the shift. Defaults to ``0``.

    Returns
    -------
    np.ndarray
        Shifted image array in same dtype as ``img``.
    """

    h, w = img.shape[:2]
    shifted = np.full_like(img, fill)
    if abs(dx) < w and abs(dy) < h:
        if dx >= 0:
            src_x = slice(0, w - dx)
            dst_x = slice(dx, dx + (w - dx))
        else:
            src_x = slice(-dx, w)
            dst_x = slice(0, w + dx)

        if dy >= 0:
            src_y = slice(0, h - dy)
            dst_y = slice(dy, dy + (h - dy))
        else:
            src_y = slice(-dy, h)
            dst_y = slice(0, h + dy)

        shifted[dst_y, dst_x, ...] = img[src_y, src_x, ...]

    return shifted
