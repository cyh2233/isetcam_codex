"""Convert an optical image illuminant to spatial-spectral format."""

from __future__ import annotations

import numpy as np

from .oi_class import OpticalImage
from .oi_illuminant_pattern import oi_illuminant_pattern


def oi_illuminant_ss(oi: OpticalImage, pattern: np.ndarray | None = None) -> OpticalImage:  # noqa: E501
    """Ensure the optical image illuminant is spatial-spectral.

    Parameters
    ----------
    oi : OpticalImage
        Input optical image with an ``illuminant`` attribute.
    pattern : array-like, optional
        Spatial pattern applied after conversion.

    Returns
    -------
    OpticalImage
        Optical image with spatial-spectral illuminant, optionally scaled by ``pattern``.  # noqa: E501
    """

    photons = np.asarray(oi.photons, dtype=float)
    rows, cols, n_wave = photons.shape

    illum = getattr(oi, "illuminant", None)
    if illum is None:
        raise AttributeError("oi has no illuminant attribute")
    ill = np.asarray(illum, dtype=float)

    if ill.ndim == 1:
        if ill.size != n_wave:
            raise ValueError("Illuminant vector length must match oi wave")
        ill_cube = np.tile(ill.reshape(1, 1, -1), (rows, cols, 1))
    elif ill.ndim == 3:
        if ill.shape != photons.shape:
            raise ValueError("Illuminant cube must match oi photon shape")
        ill_cube = ill
    else:
        raise ValueError("Illuminant must be 1-D or 3-D")

    out = OpticalImage(photons=photons, wave=oi.wave, name=oi.name)
    out.illuminant = ill_cube

    if pattern is not None:
        out = oi_illuminant_pattern(out, pattern)

    return out
