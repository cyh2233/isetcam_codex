# mypy: ignore-errors
"""Crop black border from an image."""

from __future__ import annotations

import numpy as np
from typing import Union


def image_crop_border(img: np.ndarray, threshold: float = 0.06) -> np.ndarray:
    """Return ``img`` cropped to its non-dark region.

    Parameters
    ----------
    img : np.ndarray
        Image data array. Can be 2-D or 3-D.
    threshold : float, optional
        Normalized threshold used to detect the border. Defaults to ``0.06``.

    Returns
    -------
    np.ndarray
        Cropped image. If no non-dark region is found the original image is
        returned.
    """

    if img.ndim == 3:
        gray = 0.2989 * img[..., 0] + 0.5870 * img[..., 1] + 0.1140 * img[..., 2]
    else:
        gray = img.astype(float)

    binary = gray > threshold
    rows, cols = np.where(binary)
    if rows.size == 0 or cols.size == 0:
        return img
    row1, row2 = rows.min(), rows.max()
    col1, col2 = cols.min(), cols.max()
    if row2 > row1 and col2 > col1:
        return img[row1 : row2 + 1, col1 : col2 + 1, ...]
    return img
