# mypy: ignore-errors
"""Flip an image array horizontally or vertically."""

from __future__ import annotations

import numpy as np


def image_flip(img: np.ndarray, flip_type: str) -> np.ndarray:
    """Flip ``img``.

    Parameters
    ----------
    img : np.ndarray
        Image data array. Can be 2-D or 3-D.
    flip_type : str
        ``'updown'`` for vertical flip or ``'leftright'`` for horizontal flip.
        The first character is sufficient.

    Returns
    -------
    np.ndarray
        Flipped image array.
    """

    if flip_type is None:
        raise ValueError("flip_type required")
    ft = flip_type.lower()
    if ft.startswith("u"):
        return np.flip(img, axis=0)
    if ft.startswith("l"):
        return np.flip(img, axis=1)
    raise ValueError("flip_type must be 'updown' or 'leftright'")
