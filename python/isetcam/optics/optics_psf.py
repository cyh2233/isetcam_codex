# mypy: ignore-errors
"""Convert a point spread function (PSF) to an optical transfer function (OTF)."""

from __future__ import annotations

import numpy as np
from scipy.fft import fft2, ifftshift


_DEF_ATOL = 1e-12


def optics_psf(psf: np.ndarray) -> np.ndarray:
    """Return the frequency domain OTF of ``psf``.

    The PSF is assumed to be centered. The returned OTF has the zero
    frequency component at the (0, 0) index, following the ISETCam
    convention. Energy is preserved so that ``otf[0, 0]`` equals one.
    """
    psf = np.asarray(psf, dtype=float)
    if psf.ndim < 2:
        raise ValueError("psf must have at least 2 dimensions")

    out = np.zeros(psf.shape, dtype=complex)
    if psf.ndim == 2:
        psf2 = psf / np.sum(psf)
        out = fft2(ifftshift(psf2))
    else:
        for i in range(psf.shape[-1]):
            plane = psf[..., i]
            plane = plane / np.sum(plane)
            out[..., i] = fft2(ifftshift(plane))
    return out
