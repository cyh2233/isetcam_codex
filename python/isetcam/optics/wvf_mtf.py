# mypy: ignore-errors
"""Compute the modulation transfer function from a PSF."""

from __future__ import annotations

import numpy as np
from numpy.fft import fft2, fftshift


def wvf_mtf(psf: np.ndarray) -> np.ndarray:
    """Return the MTF corresponding to ``psf``.

    Parameters
    ----------
    psf : np.ndarray
        Point spread function. Must be real valued and centered.

    Returns
    -------
    np.ndarray
        MTF magnitude normalized to one at zero frequency.
    """
    otf = fftshift(fft2(psf / np.sum(psf)))
    mtf = np.abs(otf)
    center = tuple(s // 2 for s in psf.shape)
    mtf /= mtf[center]
    return mtf


__all__ = ["wvf_mtf"]
