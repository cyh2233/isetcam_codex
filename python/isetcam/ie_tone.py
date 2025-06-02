# mypy: ignore-errors
"""Tone curve utilities."""

from __future__ import annotations

import numpy as np

from .rgb_to_xw_format import rgb_to_xw_format
from .xw_to_rgb_format import xw_to_rgb_format


def ie_tone_curve(
    num_points: int = 256,
    *,
    contrast: float = 4.0,
    midpoint: float = 0.5,
    toe: float = 0.0,
    shoulder: float = 1.0,
) -> np.ndarray:
    """Generate an S-shaped tone curve using a logistic function.

    Parameters
    ----------
    num_points : int, optional
        Number of samples in the curve, by default ``256``.
    contrast : float, optional
        Slope of the curve at ``midpoint``.
    midpoint : float, optional
        Location of the inflection point in ``[0, 1]``.
    toe : float, optional
        Minimum output value of the curve.
    shoulder : float, optional
        Maximum output value of the curve.

    Returns
    -------
    np.ndarray
        Tone curve sampled at ``num_points`` positions.
    """
    x = np.linspace(0, 1, num_points)
    y = 1 / (1 + np.exp(-contrast * (x - midpoint)))
    y = (y - y.min()) / (y.max() - y.min())
    y = y * (shoulder - toe) + toe
    return y


def ie_apply_tone(img: np.ndarray, curve: np.ndarray) -> np.ndarray:
    """Apply a tone curve to ``img``.

    Parameters
    ----------
    img : np.ndarray
        Image data in either ``(M, N)`` or ``(R, C, 3)`` format. Values are
        expected to be in the range ``[0, 1]``.
    curve : np.ndarray
        Lookup table mapping input values to output values. Can be ``(L,)`` or
        ``(L, C)`` where ``L`` is the number of levels and ``C`` is ``1`` or
        matches the number of image channels.

    Returns
    -------
    np.ndarray
        Image after tone mapping in the same shape as ``img``.
    """
    img = np.asarray(img, dtype=float)

    if img.ndim == 3:
        xw, rows, cols = rgb_to_xw_format(img)
        reshape = True
    elif img.ndim == 2:
        xw = img
        reshape = False
    else:
        raise ValueError("img must be a 2-D or 3-D array")

    tbl = np.asarray(curve, dtype=float)
    if tbl.ndim == 1:
        tbl = tbl[:, np.newaxis]
    n_levels, t_channels = tbl.shape
    n_channels = xw.shape[1]

    if t_channels == 1 and n_channels > 1:
        tbl = np.tile(tbl, (1, n_channels))
    elif t_channels != n_channels:
        raise ValueError("Tone curve channel mismatch with image")

    idx = np.clip(np.round(xw * (n_levels - 1)).astype(int), 0, n_levels - 1)
    out = np.empty_like(xw)
    for i in range(n_channels):
        out[:, i] = tbl[idx[:, i], i]

    if reshape:
        out = xw_to_rgb_format(out, rows, cols)
    return out


__all__ = ["ie_tone_curve", "ie_apply_tone"]
