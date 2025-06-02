# mypy: ignore-errors
"""Rotate the photon data of an OpticalImage."""

from __future__ import annotations

from scipy.ndimage import rotate as nd_rotate

from .oi_class import OpticalImage


def oi_rotate(oi: OpticalImage, angle: float, fill: float = 0) -> OpticalImage:
    """Rotate ``oi`` by ``angle`` degrees.

    Parameters
    ----------
    oi : OpticalImage
        Input optical image to rotate.
    angle : float
        Rotation angle in degrees. Positive values rotate counter-clockwise.
    fill : float, optional
        Value used to fill areas created by the rotation. Defaults to 0.

    Returns
    -------
    OpticalImage
        New optical image containing the rotated photon data with the same
        wavelength samples and name.
    """

    rotated = nd_rotate(
        oi.photons,
        angle,
        axes=(1, 0),
        reshape=True,
        order=1,
        mode="constant",
        cval=float(fill),
    )
    return OpticalImage(photons=rotated, wave=oi.wave, name=oi.name)
