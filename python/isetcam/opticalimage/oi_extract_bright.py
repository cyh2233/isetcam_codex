"""Extract pixels above a threshold from an :class:`OpticalImage`."""

from __future__ import annotations

import numpy as np

from .oi_class import OpticalImage


def oi_extract_bright(oi: OpticalImage, threshold: float) -> OpticalImage:
    """Return a new optical image with low photon values removed.

    Parameters
    ----------
    oi : OpticalImage
        Input optical image to subset.
    threshold : float
        Photon values below this threshold are set to zero.

    Returns
    -------
    OpticalImage
        Optical image with photon data masked by ``threshold``.
    """
    photons = np.asarray(oi.photons, dtype=float)
    masked = np.where(photons >= float(threshold), photons, 0.0)
    return OpticalImage(photons=masked, wave=oi.wave, name=oi.name)
