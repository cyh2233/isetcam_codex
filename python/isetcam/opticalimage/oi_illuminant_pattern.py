"""Apply a spatial pattern to the optical image illuminant and photons."""

from __future__ import annotations

import numpy as np
from scipy.ndimage import zoom as nd_zoom

from .oi_class import OpticalImage


def oi_illuminant_pattern(oi: OpticalImage, pattern: np.ndarray) -> OpticalImage:
    """Multiply ``oi`` photons and illuminant by ``pattern``.

    Parameters
    ----------
    oi : OpticalImage
        Input optical image containing an ``illuminant`` attribute.
    pattern : array-like
        2-D spatial pattern used to modulate the photons and illuminant.

    Returns
    -------
    OpticalImage
        New optical image with scaled photons and illuminant.
    """

    pat = np.asarray(pattern, dtype=float)
    if pat.ndim != 2:
        raise ValueError("pattern must be 2-D")

    photons = np.asarray(oi.photons, dtype=float)
    rows, cols = photons.shape[:2]
    if pat.shape != (rows, cols):
        zoom_factors = (rows / pat.shape[0], cols / pat.shape[1])
        pat = nd_zoom(pat, zoom_factors, order=1)

    scaled_photons = photons * pat[:, :, np.newaxis]
    out = OpticalImage(photons=scaled_photons, wave=oi.wave, name=oi.name)

    illum = getattr(oi, "illuminant", None)
    if illum is not None:
        ill = np.asarray(illum, dtype=float)
        if ill.ndim == 1:
            if ill.size != photons.shape[2]:
                raise ValueError("Illuminant vector length must match oi wave")
            ill = np.tile(ill.reshape(1, 1, -1), (rows, cols, 1))
        elif ill.ndim == 3:
            if ill.shape != photons.shape:
                raise ValueError("Illuminant cube must match oi photon shape")
        else:
            raise ValueError("Illuminant must be 1-D or 3-D")
        ill = ill * pat[:, :, np.newaxis]
        if np.allclose(ill, ill[0, 0, :]):
            out.illuminant = ill[0, 0, :]
        else:
            out.illuminant = ill

    return out
