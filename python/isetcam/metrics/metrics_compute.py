# mypy: ignore-errors
"""Compute common image quality metrics."""

from __future__ import annotations

import numpy as np
from typing import Sequence

from .delta_e_ab import delta_e_ab
from .delta_e_uv import delta_e_uv
from .ie_psnr import ie_psnr
from .scielab import scielab, sc_params, SCIELABParams
from ..xyz_to_lab import xyz_to_lab
from ..xyz_to_luv import xyz_to_luv


def _parse_whitepoint(white_point: Sequence[np.ndarray] | np.ndarray | None) -> tuple[np.ndarray, np.ndarray]:
    if white_point is None:
        raise ValueError("white_point is required")

    if isinstance(white_point, Sequence) and not isinstance(white_point, np.ndarray):
        if len(white_point) != 2:
            raise ValueError("white_point must have 2 elements when given as a sequence")
        wp1 = np.asarray(white_point[0], dtype=float).reshape(3)
        wp2 = np.asarray(white_point[1], dtype=float).reshape(3)
    else:
        wp1 = wp2 = np.asarray(white_point, dtype=float).reshape(3)
    return wp1, wp2


def metrics_compute(
    img1: np.ndarray,
    img2: np.ndarray,
    method: str,
    *,
    white_point: Sequence[np.ndarray] | np.ndarray | None = None,
    params: SCIELABParams | None = None,
    delta_e_version: str = "2000",
) -> np.ndarray | float:
    """Compute image quality metric between ``img1`` and ``img2``.

    Supported ``method`` values are ``"cielab"``, ``"cieluv"``, ``"mse"``,
    ``"rmse"``, ``"psnr"`` and ``"scielab"``.
    """
    img1 = np.asarray(img1, dtype=float)
    img2 = np.asarray(img2, dtype=float)
    if img1.shape != img2.shape:
        raise ValueError("img1 and img2 must have the same shape")

    m = method.lower()
    if m == "cielab":
        wp1, wp2 = _parse_whitepoint(white_point)
        lab1 = xyz_to_lab(img1, wp1)
        lab2 = xyz_to_lab(img2, wp2)
        return delta_e_ab(lab1, lab2, delta_e_version)
    elif m == "cieluv":
        wp1, wp2 = _parse_whitepoint(white_point)
        luv1 = xyz_to_luv(img1, wp1)
        luv2 = xyz_to_luv(img2, wp2)
        return delta_e_uv(luv1, luv2)
    elif m == "mse":
        diff = img1 - img2
        if diff.ndim == 3:
            return np.sum(diff ** 2, axis=-1)
        else:
            return diff ** 2
    elif m == "rmse":
        diff = img1 - img2
        if diff.ndim == 3:
            return np.sqrt(np.sum(diff ** 2, axis=-1))
        else:
            return np.abs(diff)
    elif m == "psnr":
        return float(ie_psnr(img1, img2))
    elif m == "scielab":
        if white_point is None:
            raise ValueError("white_point is required for scielab")
        if params is None:
            params = sc_params()
        return scielab(img1, img2, white_point, params)
    else:
        raise ValueError(f"Unknown metric: {method}")


__all__ = ["metrics_compute"]
