# mypy: ignore-errors
"""Rotate an image array."""

from __future__ import annotations

import numpy as np
from scipy.ndimage import rotate as nd_rotate
from typing import Union


def image_rotate(img: np.ndarray, rot_type: Union[str, float], fill: float = 0) -> np.ndarray:
    """Rotate ``img``.

    Parameters
    ----------
    img : np.ndarray
        Image data array. Can be 2-D or 3-D.
    rot_type : Union[str, float]
        If ``'cw'`` or ``'clockwise'`` rotate 90 degrees clockwise.
        If ``'ccw'`` or ``'counterclockwise'`` rotate 90 degrees
        counter-clockwise. Otherwise interpreted as rotation angle in
        degrees. Positive values rotate counter-clockwise.
    fill : float, optional
        Fill value used for regions introduced by rotation. Defaults to ``0``.

    Returns
    -------
    np.ndarray
        Rotated image array in floating point format.
    """

    if isinstance(rot_type, str):
        rt = rot_type.lower()
        if rt in {"cw", "clockwise"}:
            return np.rot90(img, k=-1, axes=(0, 1))
        if rt in {"ccw", "counterclockwise"}:
            return np.rot90(img, k=1, axes=(0, 1))
        raise ValueError("Unknown rotation type")

    rotated = nd_rotate(
        img,
        float(rot_type),
        axes=(1, 0),
        reshape=True,
        order=1,
        mode="constant",
        cval=float(fill),
    )
    return rotated
