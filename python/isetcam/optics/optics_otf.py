# mypy: ignore-errors
"""Convert an optical transfer function (OTF) to a point spread function (PSF)."""

from __future__ import annotations

import numpy as np
from scipy.fft import ifft2, fftshift


_DEF_ATOL = 1e-12


def optics_otf(otf: np.ndarray) -> np.ndarray:
    """Return the spatial PSF derived from ``otf``.

    ``otf`` should have the zero frequency component at index ``(0, 0)``.
    The returned PSF is centered and real valued. Energy is preserved so
    that the PSF sums to one.
    """
    otf = np.asarray(otf)
    if otf.ndim < 2:
        raise ValueError("otf must have at least 2 dimensions")

    out = np.zeros(otf.shape, dtype=float)
    if otf.ndim == 2:
        psf = fftshift(ifft2(otf))
        psf = np.real(psf)
        psf /= np.sum(psf)
        out = psf
    else:
        for i in range(otf.shape[-1]):
            psf = fftshift(ifft2(otf[..., i]))
            psf = np.real(psf)
            psf /= np.sum(psf)
            out[..., i] = psf
    return out
