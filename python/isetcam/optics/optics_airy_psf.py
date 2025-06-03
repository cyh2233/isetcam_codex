# mypy: ignore-errors
"""Generate an Airy disk point spread function."""

from __future__ import annotations

import numpy as np
from scipy.special import j1


def optics_airy_psf(size: int, radius: float) -> np.ndarray:
    """Return an Airy disk PSF.

    Parameters
    ----------
    size : int
        Side length of the square PSF array. Should be odd for symmetry.
    radius : float
        Pixel radius of the first zero crossing of the Airy pattern.

    Returns
    -------
    np.ndarray
        Normalized PSF of shape ``(size, size)``.
    """
    if size <= 0:
        raise ValueError("size must be positive")
    ax = np.linspace(-(size // 2), size // 2, size)
    xx, yy = np.meshgrid(ax, ax)
    r = np.hypot(xx, yy)
    r_norm = np.pi * r / float(radius)
    psf = np.ones_like(r)
    mask = r != 0
    psf[mask] = (2 * j1(r_norm[mask]) / r_norm[mask]) ** 2
    psf /= psf.sum()
    return psf


__all__ = ["optics_airy_psf"]
