"""Determine whether an image is in RGB or XW format."""

from typing import Optional
import numpy as np


def vc_get_image_format(data: np.ndarray, wave: np.ndarray) -> Optional[str]:
    """Determine the ISET image format, either ``'RGB'`` or ``'XW'``.

    Parameters
    ----------
    data : np.ndarray
        Image data either in RGB (height x width x n_wave) or XW (n_pixels x n_wave)
        format.
    wave : np.ndarray
        Vector of wavelength samples.

    Returns
    -------
    Optional[str]
        ``'RGB'`` if data appears to be in RGB format, ``'XW'`` if in XW format,
        otherwise ``None``.
    """
    wave = np.asarray(wave)

    if data.ndim == 3 and len(wave) == data.shape[2]:
        return 'RGB'
    if data.ndim == 2 and len(wave) == 1:
        return 'RGB'
    if data.ndim == 2 and len(wave) == data.shape[1]:
        return 'XW'
    if data.ndim == 1 and data.size == len(wave):
        return 'XW'
    return None
