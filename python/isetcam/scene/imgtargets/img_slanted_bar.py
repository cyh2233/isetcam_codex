# mypy: ignore-errors
"""Generate a binary slanted bar pattern image."""

from __future__ import annotations

import numpy as np


def img_slanted_bar(im_size: int = 384, bar_slope: float = 2.6) -> np.ndarray:
    """Return a binary slanted bar image.

    Parameters
    ----------
    im_size : int, optional
        Approximate size of the square image in pixels. The actual
        output dimensions are ``2 * round(im_size / 2) + 1``.
    bar_slope : float, optional
        Slope of the separating line ``y = bar_slope * x``. Pixels with
        ``y`` greater than the line are set to ``1``.
    """
    half = int(round(im_size / 2))
    rng = np.arange(-half, half + 1)
    X, Y = np.meshgrid(rng, rng)
    img = (Y > bar_slope * X).astype(float)
    img = np.clip(img, 1e-6, 1.0)
    return img


__all__ = ["img_slanted_bar"]
