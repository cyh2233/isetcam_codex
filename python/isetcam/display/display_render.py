"""Render display spectral output from digital RGB values."""

from __future__ import annotations

import numpy as np

from .display_class import Display
from .display_apply_gamma import display_apply_gamma
from ..rgb_to_xw_format import rgb_to_xw_format
from ..xw_to_rgb_format import xw_to_rgb_format


def display_render(image: np.ndarray, display: Display, apply_gamma: bool = True) -> np.ndarray:  # noqa: E501
    """Return spectral radiance for ``image`` on ``display``.

    Parameters
    ----------
    image : np.ndarray
        Digital RGB image values in ``(R, C, 3)`` or ``(N, 3)`` format.
    display : Display
        Display providing spectral primaries and optional gamma table.
    apply_gamma : bool, optional
        When ``True`` apply ``display``'s gamma table to ``image`` before
        computing the spectral radiance.

    Returns
    -------
    np.ndarray
        Spectral radiance image with one band per display wavelength.
        The output has the same spatial organisation as ``image``.
    """
    img = np.asarray(image, dtype=float)

    if img.ndim == 3:
        reshape = True
        xw, rows, cols = rgb_to_xw_format(img)
    elif img.ndim == 2 and img.shape[1] == 3:
        reshape = False
        xw = img
    else:
        raise ValueError("image must be (rows, cols, 3) or (n, 3)")

    if apply_gamma and display.gamma is not None:
        xw = display_apply_gamma(xw, display)

    spd = np.asarray(display.spd, dtype=float)
    if spd.shape[1] != 3:
        raise ValueError("display.spd must have shape (n_wave, 3)")

    out_xw = xw @ spd.T

    if reshape:
        out = xw_to_rgb_format(out_xw, rows, cols)
    else:
        out = out_xw

    return out
