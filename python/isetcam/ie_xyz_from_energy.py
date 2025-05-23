"""Compute CIE XYZ tristimulus values from spectral energy."""

from __future__ import annotations

from pathlib import Path
import numpy as np
from scipy.io import loadmat

from .vc_get_image_format import vc_get_image_format
from .rgb_to_xw_format import rgb_to_xw_format
from .xw_to_rgb_format import xw_to_rgb_format


def _xyz_color_matching(wave: np.ndarray) -> np.ndarray:
    """Interpolate the CIE XYZ color matching functions to ``wave``."""
    root = Path(__file__).resolve().parents[2]
    data = loadmat(root / "data" / "human" / "XYZ.mat")
    src_wave = data["wavelength"].ravel()
    xyz = data["data"]
    cmf = np.zeros((len(wave), 3))
    for i in range(3):
        cmf[:, i] = np.interp(wave, src_wave, xyz[:, i], left=0.0, right=0.0)
    return cmf


def ie_xyz_from_energy(energy: np.ndarray, wavelength: np.ndarray) -> np.ndarray:
    """Convert spectral energy to CIE XYZ.

    Parameters
    ----------
    energy : np.ndarray
        Spectral energy with wavelength along the last dimension for RGB format
        or in columns for XW format.
    wavelength : array-like
        Sampled wavelengths in nanometers.

    Returns
    -------
    np.ndarray
        XYZ values in the same spatial format as ``energy``.
    """
    energy = np.asarray(energy)
    if energy.size == 0:
        return np.array([])

    wave = np.asarray(wavelength).reshape(-1)
    cmf = _xyz_color_matching(wave)

    img_format = vc_get_image_format(energy, wave)
    if img_format == "RGB":
        xw, r, c = rgb_to_xw_format(energy)
    else:
        if energy.ndim == 1:
            xw = energy[np.newaxis, :]
        else:
            xw = energy
        r = c = None
    if xw.shape[1] != len(wave):
        raise ValueError("Energy must be arranged with wavelength columns")

    binwidth = wave[1] - wave[0] if len(wave) > 1 else 10
    xyz = 683 * xw.dot(cmf) * binwidth

    if img_format == "RGB":
        return xw_to_rgb_format(xyz, r, c)
    return xyz
