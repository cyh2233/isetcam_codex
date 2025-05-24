"""Peak signal-to-noise ratio between two images."""

from __future__ import annotations

import numpy as np


def ie_psnr(im1: np.ndarray, im2: np.ndarray) -> float:
    """Compute PSNR value consistent with MATLAB ``iePSNR``.

    Parameters
    ----------
    im1, im2 : np.ndarray
        Images to compare. They must have the same shape.

    Returns
    -------
    float
        PSNR value in decibels. ``np.inf`` is returned when the images are
        identical.
    """
    im1 = np.asarray(im1, dtype=float)
    im2 = np.asarray(im2, dtype=float)
    if im1.shape != im2.shape:
        raise ValueError("Input images must have the same shape")

    se = (255 * (im1 - im2)) ** 2
    rmse = np.sqrt(np.mean(se))

    if rmse == 0:
        return np.inf

    return 20 * np.log10(255 / np.sqrt(rmse))
