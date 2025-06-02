"""Optical image diffusers."""

from __future__ import annotations

from typing import Sequence

import numpy as np
from scipy.ndimage import gaussian_filter, shift as nd_shift

from .oi_class import OpticalImage


def _get_spacing_um(oi: OpticalImage) -> float:
    spacing = getattr(oi, "sample_spacing", 1.0)
    return float(spacing) * 1e6


def oi_diffuser(oi: OpticalImage, blur_um: Sequence[float] | float, method: str = "gaussian") -> OpticalImage:
    """Apply a diffuser to ``oi``.

    Parameters
    ----------
    oi : OpticalImage
        Input optical image to blur.
    blur_um : float or sequence of float
        Blur amount in microns.  For the Gaussian method this specifies the
        standard deviation of the blur kernel.  A scalar value applies the
        same blur in row and column directions while two values may be used
        for an anisotropic blur.  For the birefringent method this specifies
        the displacement of the shifted copies.
    method : {"gaussian", "birefringent"}, optional
        Diffuser type. Defaults to ``"gaussian"``.

    Returns
    -------
    OpticalImage
        New optical image containing the blurred photons.
    """
    method = method.lower()
    if method == "gaussian":
        spacing_um = _get_spacing_um(oi)
        sigma = np.asarray(blur_um, dtype=float)
        if sigma.ndim == 0:
            sigma = np.array([sigma, sigma])
        if sigma.size != 2:
            raise ValueError("blur_um must be a scalar or length-2 sequence")
        sigma_pix = sigma / spacing_um
        blurred = gaussian_filter(oi.photons, sigma=(sigma_pix[0], sigma_pix[1], 0))
        return OpticalImage(photons=blurred, wave=oi.wave, name=oi.name)
    elif method == "birefringent":
        return oi_birefringent_diffuser(oi, float(np.asarray(blur_um).ravel()[0]))
    else:
        raise ValueError("Unknown diffuser method")


def oi_birefringent_diffuser(
    oi: OpticalImage, blur_um: float, orientation: float = 0
) -> OpticalImage:
    """Apply a birefringent diffuser to ``oi``.

    This simulates the effect of a birefringent filter by averaging four
    shifted copies of the optical image.  The copies are displaced by
    ``blur_um`` microns along ``orientation`` and the perpendicular
    direction.

    Parameters
    ----------
    oi : OpticalImage
        Input optical image.
    blur_um : float
        Displacement of the shifted copies in microns.
    orientation : float, optional
        Orientation angle of the displacement in degrees. Defaults to 0.

    Returns
    -------
    OpticalImage
        Optical image containing the blurred photons.
    """

    spacing_um = _get_spacing_um(oi)
    delta = float(blur_um) / spacing_um

    theta = np.deg2rad(float(orientation))
    rot = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])

    base = np.array(
        [
            [delta, delta],
            [-delta, delta],
            [delta, -delta],
            [-delta, -delta],
        ]
    )
    shifts = base @ rot.T

    accum = np.zeros_like(oi.photons, dtype=float)
    for dx, dy in shifts:
        shifted = nd_shift(
            oi.photons,
            shift=(dy, dx, 0),
            order=1,
            mode="constant",
            cval=0.0,
        )
        accum += shifted
    accum /= shifts.shape[0]

    return OpticalImage(photons=accum, wave=oi.wave, name=oi.name)


__all__ = ["oi_diffuser", "oi_birefringent_diffuser"]
