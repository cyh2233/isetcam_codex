# mypy: ignore-errors
"""Structural Similarity (SSIM) image quality metric."""

from __future__ import annotations

import numpy as np
from skimage.metrics import structural_similarity


def ssim_metric(img1: np.ndarray, img2: np.ndarray) -> tuple[float, np.ndarray]:
    """Return SSIM value and per-pixel map between ``img1`` and ``img2``.

    Parameters
    ----------
    img1, img2 : np.ndarray
        Input images with the same shape. Values are assumed to lie in
        the range [0, 1].

    Returns
    -------
    float
        Overall SSIM value.
    np.ndarray
        SSIM map with the same shape as the inputs.
    """
    img1 = np.asarray(img1, dtype=float)
    img2 = np.asarray(img2, dtype=float)
    if img1.shape != img2.shape:
        raise ValueError("Input images must have the same shape")

    kwargs = {"data_range": 1.0}
    if img1.ndim == 3:
        kwargs["channel_axis"] = -1
    score, s_map = structural_similarity(img1, img2, full=True, **kwargs)
    return score, s_map


__all__ = ["ssim_metric"]
