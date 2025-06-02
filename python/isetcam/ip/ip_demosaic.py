# mypy: ignore-errors
"""Convenience wrapper for basic demosaicing algorithms."""

from __future__ import annotations

import numpy as np

from ..imgproc import (
    ie_nearest_neighbor,
    ie_bilinear,
    adaptive_laplacian,
    pocs,
)


def ip_demosaic(
    bayer: np.ndarray,
    pattern: str = "rggb",
    method: str = "bilinear",
) -> np.ndarray:
    """Demosaic a Bayer-pattern image using ``method``.

    Parameters
    ----------
    bayer : np.ndarray
        2-D array containing the raw mosaic image.
    pattern : str, optional
        CFA pattern string such as ``"rggb"``. Defaults to ``"rggb"``.
    method : str, optional
        Demosaicing method. One of ``'nearest'``, ``'bilinear'``,
        ``'adaptive'`` (adaptive Laplacian) or ``'pocs'``.
        Defaults to ``'bilinear'``.

    Returns
    -------
    np.ndarray
        RGB image with shape ``(rows, cols, 3)``.
    """
    funcs = {
        "nearest": ie_nearest_neighbor,
        "nearest_neighbor": ie_nearest_neighbor,
        "bilinear": ie_bilinear,
        "adaptive": adaptive_laplacian,
        "adaptive_laplacian": adaptive_laplacian,
        "laplacian": adaptive_laplacian,
        "pocs": pocs,
    }
    key = method.lower()
    if key not in funcs:
        raise ValueError("Unknown demosaic method")
    return funcs[key](bayer, pattern)


__all__ = ["ip_demosaic"]
