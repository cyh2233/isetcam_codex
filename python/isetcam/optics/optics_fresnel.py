# mypy: ignore-errors
"""Simple scalar Fresnel propagation."""

from __future__ import annotations

import numpy as np
from numpy.fft import fft2, ifft2, fftshift, ifftshift, fftfreq


def optics_fresnel(field: np.ndarray, dx: float, wavelength: float, distance: float) -> np.ndarray:
    """Propagate ``field`` by ``distance`` using the Fresnel approximation.

    Parameters
    ----------
    field : np.ndarray
        Complex input field sampled on a square grid.
    dx : float
        Sample spacing in meters.
    wavelength : float
        Wavelength of light in meters.
    distance : float
        Propagation distance in meters.

    Returns
    -------
    np.ndarray
        Propagated complex field with the same shape as ``field``.
    """
    ny, nx = field.shape
    fx = fftfreq(nx, dx)
    fy = fftfreq(ny, dx)
    FX, FY = np.meshgrid(fx, fy)
    H = np.exp(-1j * np.pi * wavelength * distance * (FX ** 2 + FY ** 2))
    F = fft2(ifftshift(field))
    out = fftshift(ifft2(F * H))
    return out


__all__ = ["optics_fresnel"]
