"""Visual signal-to-noise ratio in the S-CIELAB domain."""

from __future__ import annotations

import numpy as np
from typing import Sequence

from .scielab import SCIELABParams, sc_params, _sc_prepare_filters, _sc_opponent_filter
from ..xyz_to_lab import xyz_to_lab


def _clip_xyz_image(xyz: np.ndarray, white: Sequence[float]) -> np.ndarray:
    xyz = np.asarray(xyz, dtype=float)
    white = np.asarray(white, dtype=float).reshape(3)
    clipped = np.clip(xyz, 0, white)
    return clipped


def _get_middle_matrix(m: np.ndarray, size: Sequence[int]) -> np.ndarray:
    size = np.array(size, dtype=int)
    half = np.round(size / 2).astype(int)
    if half.size == 1:
        half = np.array([half[0], half[0]])
    center = (np.array(m.shape[:2]) + 1) // 2 - 1
    r_min = max(0, center[0] - half[0])
    r_max = min(m.shape[0], center[0] + half[0] + 1)
    c_min = max(0, center[1] - half[1])
    c_max = min(m.shape[1], center[1] + half[1] + 1)
    return m[r_min:r_max, c_min:c_max, ...]


def _sc_compute_scielab(xyz: np.ndarray, white: Sequence[float], params: SCIELABParams) -> np.ndarray:
    xyz = _clip_xyz_image(xyz, white)
    if params.filters is None:
        params.filters, _ = _sc_prepare_filters(params)
    filtered = _sc_opponent_filter(xyz, params)
    return xyz_to_lab(filtered, white)


def xyz_to_vsnr(
    roi_xyz: np.ndarray,
    white_point: Sequence[float],
    params: SCIELABParams | None = None,
) -> float:
    """Compute visual SNR from an XYZ image.

    Parameters
    ----------
    roi_xyz : np.ndarray
        XYZ values of the region of interest.
    white_point : sequence of float
        Display white point in XYZ.
    params : :class:`~isetcam.metrics.SCIELABParams`, optional
        Parameters controlling the S-CIELAB calculation. When ``None`` the
        defaults from :func:`sc_params` are used.
    """
    if params is None:
        params = sc_params()

    s_lab = _sc_compute_scielab(roi_xyz, white_point, params)
    r, c, _ = s_lab.shape
    mid = np.round(0.8 * np.array([r, c])).astype(int)
    s_lab = _get_middle_matrix(s_lab, mid)

    L_var = np.std(s_lab[..., 0]) ** 2
    A_var = np.std(s_lab[..., 1]) ** 2
    B_var = np.std(s_lab[..., 2]) ** 2

    return 1.0 / np.sqrt(L_var + A_var + B_var)


__all__ = ["xyz_to_vsnr"]
