# mypy: ignore-errors
"""Simple threshold dithering halftoning."""

from __future__ import annotations

import numpy as np

from ..ie_scale import ie_scale


def halftone_dither(cell: np.ndarray, image: np.ndarray) -> np.ndarray:
    """Halftone ``image`` using the provided dither ``cell``.

    Parameters
    ----------
    cell : np.ndarray
        Halftone threshold matrix. If the maximum value exceeds ``1`` it is
        linearly scaled into the range ``[0, 1]``.
    image : np.ndarray
        2-D grayscale image with values between ``0`` and ``1``.

    Returns
    -------
    np.ndarray
        Binary halftoned image of the same shape as ``image``.
    """
    cell = np.asarray(cell, dtype=float)
    img = np.asarray(image, dtype=float)

    if cell.max() > 1:
        low = 0.5 / float(cell.max())
        high = 1.0 - low
        cell, _, _ = ie_scale(cell, low, high)

    cell_rows, cell_cols = cell.shape
    img_rows, img_cols = img.shape

    r = int(np.ceil(img_rows / cell_rows))
    c = int(np.ceil(img_cols / cell_cols))
    mask = np.tile(cell, (r, c))
    mask = mask[:img_rows, :img_cols]

    return (mask < img).astype(int)


__all__ = ["halftone_dither"]
