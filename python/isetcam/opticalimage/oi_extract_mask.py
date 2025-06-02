"""Extract a masked region from an :class:`OpticalImage`."""

from __future__ import annotations

import numpy as np

from .oi_class import OpticalImage


def oi_extract_mask(oi: OpticalImage, mask: np.ndarray) -> OpticalImage:
    """Return a new optical image with photon data outside ``mask`` removed.

    Parameters
    ----------
    oi : OpticalImage
        Input optical image to subset.
    mask : array_like
        Boolean array identifying pixels to keep. May be 2-D or 3-D.
        If 2-D, the same mask is applied to all wavelength planes.

    Returns
    -------
    OpticalImage
        Optical image with photon data masked by ``mask``.
    """
    photons = np.asarray(oi.photons, dtype=float)
    m = np.asarray(mask, dtype=bool)
    if m.ndim == 2:
        m = m[:, :, None]
    try:
        m = np.broadcast_to(m, photons.shape)
    except ValueError:
        raise ValueError("mask shape does not match photon data")
    masked = np.where(m, photons, 0.0)
    return OpticalImage(photons=masked, wave=oi.wave, name=oi.name)
