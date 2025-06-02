# mypy: ignore-errors
"""Convert image data from XW format to RGB format."""

from __future__ import annotations

from typing import Tuple
import numpy as np


def xw_to_rgb_format(im_xw: np.ndarray, rows: int, cols: int) -> np.ndarray:
    """Reshape ``im_xw`` from ``(rows*cols, bands)`` to ``(rows, cols, bands)``.

    Parameters
    ----------
    im_xw : np.ndarray
        Image data in XW format. Monochrome data may be provided as ``(rows*cols,)``.
    rows : int
        Number of image rows.
    cols : int
        Number of image columns.

    Returns
    -------
    np.ndarray
        Image data in RGB format with shape ``(rows, cols, bands)``.
    """
    im_xw = np.asarray(im_xw)
    if im_xw.ndim == 1:
        bands = 1
        if im_xw.size != rows * cols:
            raise ValueError("Input size does not match rows*cols")
        im_xw = im_xw.reshape(rows * cols, bands)
    elif im_xw.ndim == 2:
        if im_xw.shape[0] != rows * cols:
            raise ValueError("Input size does not match rows*cols")
        bands = im_xw.shape[1]
    else:
        raise ValueError("im_xw must be a 1D or 2D array")

    return im_xw.reshape(rows, cols, bands)
