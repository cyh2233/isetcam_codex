# mypy: ignore-errors
"""Simple illuminant correction routines."""

from __future__ import annotations

import numpy as np
from typing import Sequence

from ..ie_param_format import ie_param_format
from ..illuminant import illuminant_create
from ..rgb_to_xw_format import rgb_to_xw_format
from ..xw_to_rgb_format import xw_to_rgb_format


def _replace_nan(data: np.ndarray, value: float = 0.0) -> np.ndarray:
    """Return ``data`` with ``NaN`` values replaced by ``value``."""
    out = np.asarray(data, dtype=float).copy()
    out[np.isnan(out)] = value
    return out


def _image_linear_transform(im: np.ndarray, T: np.ndarray) -> np.ndarray:
    if im.ndim == 3:
        xw, r, c = rgb_to_xw_format(im)
        out = xw @ T
        return xw_to_rgb_format(out, r, c)
    if im.ndim == 2:
        if im.shape[1] != T.shape[0]:
            raise ValueError("Matrix dimensions do not align")
        return im @ T
    raise ValueError("Image must be RGB or XW format")


def _calc_wp_scaling(
    internal_cmf: np.ndarray | None,
    wave: Sequence[float] | None,
    target: str | Sequence[float] = "D65",
) -> np.ndarray:
    """Return scaling of an equal energy white in ``internal_cmf`` space."""
    if internal_cmf is None:
        return np.ones(1)

    if isinstance(target, str):
        if wave is None:
            raise ValueError("wave must be provided when target is a name")
        illum = illuminant_create(target, np.asarray(wave))
        t_data = illum.spd
    else:
        t_data = np.asarray(target, dtype=float)
    white = internal_cmf.T @ t_data
    white = white / np.max(white)
    return white


def _gray_world(img: np.ndarray, internal_cmf, wave, target) -> np.ndarray:
    img = _replace_nan(img, 0)
    N = img.shape[2]
    white_ratio = _calc_wp_scaling(internal_cmf, wave, target)
    if white_ratio.size == 1:
        white_ratio = np.ones(N)
    white_ratio = white_ratio / white_ratio[0]
    avg = img.mean(axis=(0, 1))
    D = [white_ratio[i] * (avg[0] / avg[i]) if avg[i] != 0 else 0 for i in range(N)]
    return np.diag(D)


def _white_world(img: np.ndarray, internal_cmf, wave, target) -> np.ndarray:
    img = _replace_nan(img, 0)
    N = img.shape[2]
    mx = [img[:, :, i].max() for i in range(N)]
    white_ratio = _calc_wp_scaling(internal_cmf, wave, target)
    if white_ratio.size == 1:
        white_ratio = np.ones(N)
    bright_plane_index = int(np.argmax(mx))
    bright_plane = img[:, :, bright_plane_index]
    criterion = 0.7
    brt = []
    thresh = criterion * mx[bright_plane_index]
    mask = bright_plane >= thresh
    for i in range(N):
        vals = img[:, :, i][mask]
        brt.append(vals.mean() if vals.size > 0 else 0)
    white_ratio = white_ratio / white_ratio[0]
    D = [white_ratio[i] * (brt[0] / brt[i]) if brt[i] != 0 else 0 for i in range(N)]
    return np.diag(D)


def image_illuminant_correction(
    img: np.ndarray,
    method: str = "none",
    *,
    internal_cmf: np.ndarray | None = None,
    wave: Sequence[float] | None = None,
    target_white: str | Sequence[float] = "D65",
    transform: np.ndarray | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    """Apply simple illuminant correction to ``img``."""
    method = ie_param_format(method)
    if img.size == 0:
        return img, np.eye(img.shape[2])
    if method == "none":
        T = np.eye(img.shape[2])
        return img, T
    if method == "grayworld":
        T = _gray_world(img, internal_cmf, wave, target_white)
    elif method == "whiteworld":
        T = _white_world(img, internal_cmf, wave, target_white)
    elif method in {"manualmatrixentry", "manual"}:
        if transform is None:
            raise ValueError("Manual correction requires 'transform'")
        T = np.asarray(transform, dtype=float)
    else:
        raise ValueError(f"Unknown illuminant correction method {method}")
    corrected = _image_linear_transform(img, T)
    return corrected, T

__all__ = ["image_illuminant_correction"]
