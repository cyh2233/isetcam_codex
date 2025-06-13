# mypy: ignore-errors
"""Compute inverse lookup table from linear RGB to DAC values."""

from __future__ import annotations

import numpy as np


def ie_lut_invert(in_lut: np.ndarray, n_steps: int = 2048) -> np.ndarray:
    """Return inverse lookup table of ``in_lut``.

    Parameters
    ----------
    in_lut : np.ndarray
        Lookup table mapping DAC to linear intensity.
    n_steps : int, optional
        Number of samples in the returned table. Defaults to ``2048``.

    Returns
    -------
    np.ndarray
        Inverse lookup table of shape ``(n_steps, n_channels)``.
    """

    lut = np.asarray(in_lut, dtype=float)
    if lut.ndim == 1:
        lut = lut[:, np.newaxis]

    n_in = lut.shape[0]
    y = np.arange(1, n_in + 1)
    i_y = np.linspace(0, (n_steps - 1) / n_steps, n_steps)
    out = np.zeros((n_steps, lut.shape[1]), dtype=float)
    for c in range(lut.shape[1]):
        x, idx = np.unique(lut[:, c], return_index=True)
        out[:, c] = np.interp(i_y, x, y[idx], left=0, right=n_in)
    np.clip(out, 0, n_in, out=out)
    return out
