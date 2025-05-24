"""Estimate correlated color temperature from an sRGB image."""

from __future__ import annotations

import numpy as np
from scipy.io import loadmat

from .srgb_xyz import srgb_to_xyz
from .rgb_to_xw_format import rgb_to_xw_format
from .chromaticity import chromaticity
from .iset_root_path import iset_root_path
from .illuminant import illuminant_blackbody

__all__ = ["srgb_to_cct"]


def _default_table() -> np.ndarray:
    """Return lookup table of xy chromaticities for sample color temperatures."""
    wave = np.arange(400, 701, 10)
    ctemps = np.arange(2500, 10501, 500)
    root = iset_root_path()
    data = loadmat(root / "data" / "human" / "XYZEnergy.mat")
    src_wave = data["wavelength"].ravel()
    XYZ = np.zeros((len(wave), 3))
    for i in range(3):
        XYZ[:, i] = np.interp(wave, src_wave, data["data"][:, i], left=0.0, right=0.0)

    xy = np.zeros((len(ctemps), 2))
    for i, t in enumerate(ctemps):
        spd = illuminant_blackbody(t, wave)
        cieXYZ = XYZ.T @ spd
        xy[i] = chromaticity(cieXYZ.reshape(1, 3))[0]
    return np.column_stack([ctemps, xy])


def srgb_to_cct(rgb: np.ndarray, *, table: np.ndarray | None = None) -> tuple[float, np.ndarray]:
    """Estimate correlated color temperature from an sRGB image.

    Parameters
    ----------
    rgb : np.ndarray
        sRGB image data in RGB or XW format. Values are expected in ``[0, 1]``.
    table : np.ndarray, optional
        Precomputed lookup table returned from a previous call.

    Returns
    -------
    float
        Estimated color temperature in Kelvin.
    np.ndarray
        The lookup table used for the estimation.
    """
    rgb = np.asarray(rgb, dtype=float)
    if table is None:
        table = _default_table()
    ctemps = table[:, 0]
    xy_table = table[:, 1:]

    img_xyz = srgb_to_xyz(rgb)
    if img_xyz.ndim == 3:
        xw, _, _ = rgb_to_xw_format(img_xyz)
    else:
        xw = img_xyz

    Y = xw[:, 1]
    topY = np.percentile(Y, 98)
    topXYZ = xw[Y > topY]
    topxy = chromaticity(topXYZ).mean(axis=0)

    diffs = np.linalg.norm(xy_table - topxy, axis=1)
    idx = np.argmin(diffs)
    return float(ctemps[idx]), table
