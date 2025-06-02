# mypy: ignore-errors
"""Convert image data from RGB format to XW format."""

from __future__ import annotations

import numpy as np
from typing import Tuple


def rgb_to_xw_format(im_rgb: np.ndarray) -> Tuple[np.ndarray, int, int]:
    """Reshape ``im_rgb`` from ``(rows, cols, bands)`` to ``(rows*cols, bands)``.

    Parameters
    ----------
    im_rgb : np.ndarray
        Image data in RGB format. Monochrome images may be provided as
        ``(rows, cols)``.

    Returns
    -------
    Tuple[np.ndarray, int, int]
        ``im_xw`` array in XW format along with the original row and column
        dimensions.
    """
    im_rgb = np.asarray(im_rgb)
    if im_rgb.ndim == 2:
        rows, cols = im_rgb.shape
        bands = 1
        im_rgb = im_rgb.reshape(rows, cols, bands)
    elif im_rgb.ndim == 3:
        rows, cols, bands = im_rgb.shape
    else:
        raise ValueError("im_rgb must be a 2D or 3D array")

    im_xw = im_rgb.reshape(rows * cols, bands)
    return im_xw, rows, cols
