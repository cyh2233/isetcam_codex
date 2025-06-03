# mypy: ignore-errors
"""Generate a frequency-orientation test target image."""

from __future__ import annotations

import numpy as np
from scipy.signal import square


def img_fo_target(
    *,
    pattern: str = "sine",
    angles: np.ndarray | list[float] | None = None,
    freqs: np.ndarray | list[float] | None = None,
    block_size: int = 32,
    contrast: float = 1.0,
) -> np.ndarray:
    """Return a grayscale frequency/orientation target.

    Parameters
    ----------
    pattern : {'sine', 'square'}, optional
        Type of pattern used for each block. Defaults to ``'sine'``.
    angles : array-like, optional
        List of orientations in radians for each row of blocks.
        Defaults to ``np.linspace(0, np.pi/2, 8)``.
    freqs : array-like, optional
        List of spatial frequencies for each column of blocks.
        Defaults to ``np.arange(1, 9)``.
    block_size : int, optional
        Size in pixels of each block. Defaults to ``32``.
    contrast : float, optional
        Contrast of the sinusoid or square wave. Defaults to ``1``.

    Returns
    -------
    ndarray
        2-D array containing the target pattern scaled between 0 and 1.
    """
    if angles is None:
        angles = np.linspace(0, np.pi / 2, 8)
    else:
        angles = np.asarray(angles, dtype=float).reshape(-1)
    if freqs is None:
        freqs = np.arange(1, 9)
    else:
        freqs = np.asarray(freqs, dtype=float).reshape(-1)
    block = int(block_size)

    x = np.arange(block) / block
    X, Y = np.meshgrid(x, x)

    rows = []
    patt = pattern.lower()
    for f in freqs:
        cols = []
        for theta in angles:
            phase = 2 * np.pi * f * (np.cos(theta) * X + np.sin(theta) * Y)
            if patt == "sine":
                val = 0.5 * (1 + contrast * np.sin(phase))
            elif patt == "square":
                val = 0.5 * (1 + contrast * square(phase))
            else:
                raise ValueError(f"Unknown pattern '{pattern}'")
            cols.append(val)
        rows.append(np.concatenate(cols, axis=1))
    img = np.concatenate(rows, axis=0)
    img = img.T  # frequency increases left->right, orientation top->bottom
    img = np.clip(img, 1e-6, 1.0)
    return img


__all__ = ["img_fo_target"]
