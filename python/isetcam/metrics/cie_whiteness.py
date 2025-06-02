# mypy: ignore-errors
"""CIE 2004 whiteness index."""

from __future__ import annotations

import numpy as np
from typing import Sequence
from scipy.io import loadmat

from ..ie_xyz_from_energy import ie_xyz_from_energy
from ..chromaticity import chromaticity
from ..data_path import data_path


def _load_illuminant(name: str, wave: np.ndarray) -> np.ndarray:
    """Load illuminant SPD interpolated to ``wave``."""
    mat = loadmat(data_path(f"lights/{name}.mat"))
    src_wave = mat["wavelength"].ravel()
    spd = np.interp(wave, src_wave, mat["data"].ravel(), left=0.0, right=0.0)
    return spd


def _broadcast_spd(spd: np.ndarray, shape: Sequence[int]) -> np.ndarray:
    return spd.reshape((1,) * (len(shape) - 1) + (-1,))


def cie_whiteness(
    xyz: np.ndarray | None = None,
    *,
    reflectance: np.ndarray | None = None,
    wavelength: np.ndarray | None = None,
    illuminant: str | np.ndarray = "D65",
) -> np.ndarray:
    """Return the CIE 2004 whiteness index.

    Parameters
    ----------
    xyz : np.ndarray, optional
        CIE XYZ values with the last dimension of length 3.
    reflectance : np.ndarray, optional
        Reflectance spectra with wavelength along the final dimension.
    wavelength : np.ndarray, optional
        Wavelength sampling corresponding to ``reflectance`` when provided.
    illuminant : str or np.ndarray, optional
        Illuminant spectral power distribution. When a string, the SPD is
        loaded from ``isetcam.data/lights``. Defaults to ``"D65"``.

    Returns
    -------
    np.ndarray
        Whiteness index with the same spatial dimensions as ``xyz`` or
        ``reflectance``.
    """
    squeeze = False
    if xyz is None:
        if reflectance is None or wavelength is None:
            raise ValueError("xyz or reflectance+wavelength required")
        wave = np.asarray(wavelength).reshape(-1)
        refl = np.asarray(reflectance, dtype=float)
        if isinstance(illuminant, str):
            ill = _load_illuminant(illuminant, wave)
        else:
            ill = np.asarray(illuminant, dtype=float)
            if ill.shape != wave.shape:
                raise ValueError("illuminant must match wavelength length")
        energy = refl * _broadcast_spd(ill, refl.shape)
        xyz = ie_xyz_from_energy(energy, wave)
        white_xyz = ie_xyz_from_energy(ill.reshape(1, -1), wave)[0]
        x_n, y_n = chromaticity(white_xyz.reshape(1, 3))[0]
        Y = 100 * xyz[..., 1] / white_xyz[1]
    else:
        xyz = np.asarray(xyz, dtype=float)
        if xyz.ndim == 1:
            xyz = xyz.reshape(1, 3)
            squeeze = True
        else:
            squeeze = False
        if isinstance(illuminant, str):
            mat = loadmat(data_path(f"lights/{illuminant}.mat"))
            wave = mat["wavelength"].ravel()
            ill = mat["data"].ravel()
            white_xyz = ie_xyz_from_energy(ill.reshape(1, -1), wave)[0]
            x_n, y_n = chromaticity(white_xyz.reshape(1, 3))[0]
            Y = xyz[..., 1]
        elif wavelength is not None and np.iterable(illuminant):
            ill = np.asarray(illuminant, dtype=float)
            wave = np.asarray(wavelength).reshape(-1)
            if ill.shape != wave.shape:
                raise ValueError("illuminant must match wavelength length")
            white_xyz = ie_xyz_from_energy(ill.reshape(1, -1), wave)[0]
            x_n, y_n = chromaticity(white_xyz.reshape(1, 3))[0]
            Y = xyz[..., 1]
        else:
            x_n, y_n = 0.3127, 0.3290
            Y = xyz[..., 1]
        if squeeze:
            xyz = xyz.reshape(1, 3)
    xy = chromaticity(xyz)
    x = xy[..., 0]
    y = xy[..., 1]
    W = Y + 800 * (x_n - x) + 1700 * (y_n - y)
    if squeeze:
        return float(W[0])
    return W


__all__ = ["cie_whiteness"]
