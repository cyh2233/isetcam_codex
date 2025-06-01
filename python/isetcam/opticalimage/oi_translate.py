"""Translate the photon data of an OpticalImage."""

from __future__ import annotations

import numpy as np

from .oi_class import OpticalImage


def oi_translate(oi: OpticalImage, dx: int, dy: int, fill: float = 0) -> OpticalImage:
    """Shift ``oi`` by ``dx`` and ``dy`` pixels.

    Parameters
    ----------
    oi : OpticalImage
        Input optical image to translate.
    dx, dy : int
        Horizontal and vertical shift in pixels. Positive values move the
        image to the right and down respectively.
    fill : float, optional
        Value used to fill areas exposed by the shift. Defaults to 0.

    Returns
    -------
    OpticalImage
        New optical image containing the shifted photon data with the same
        wavelength samples and name.
    """

    photons = oi.photons
    h, w = photons.shape[:2]
    shifted = np.full_like(photons, fill, dtype=photons.dtype)

    if abs(dx) < w and abs(dy) < h:
        if dx >= 0:
            src_x = slice(0, w - dx)
            dst_x = slice(dx, dx + (w - dx))
        else:
            src_x = slice(-dx, w)
            dst_x = slice(0, w + dx)

        if dy >= 0:
            src_y = slice(0, h - dy)
            dst_y = slice(dy, dy + (h - dy))
        else:
            src_y = slice(-dy, h)
            dst_y = slice(0, h + dy)

        shifted[dst_y, dst_x, :] = photons[src_y, src_x, :]

    return OpticalImage(photons=shifted, wave=oi.wave, name=oi.name)
