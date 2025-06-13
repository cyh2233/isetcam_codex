# mypy: ignore-errors
"""Convert linear RGB values to DAC through an inverse gamma table."""

from __future__ import annotations

import numpy as np
from typing import Union


def ie_lut_linear(rgb: np.ndarray, g_table: Union[np.ndarray, float] = 2.2) -> np.ndarray:
    """Return DAC values for ``rgb`` using ``g_table``.

    Parameters
    ----------
    rgb : np.ndarray
        Linear intensity values in the range ``[0, 1]``.
    g_table : Union[np.ndarray, float], optional
        Inverse gamma table mapping linear intensity to DAC. If scalar,
        ``rgb`` values are raised to ``1/g_table``. Defaults to ``2.2``.

    Returns
    -------
    np.ndarray
        Integer DAC values.
    """

    rgb = np.asarray(rgb)
    if np.isscalar(g_table):
        return rgb.astype(float) ** (1.0 / float(g_table))

    lut = np.asarray(g_table, dtype=float)
    if lut.ndim == 1:
        lut = lut[:, np.newaxis]
    n_levels = lut.shape[0]

    rgb_idx = np.clip((rgb * n_levels).astype(int), 0, n_levels - 1)

    if lut.shape[1] == 1 and rgb.ndim == 3:
        lut = np.tile(lut, (1, rgb.shape[2]))

    if rgb.ndim == 2:
        return lut[rgb_idx, 0]

    dac = np.empty_like(rgb_idx, dtype=float)
    for c in range(rgb.shape[2]):
        dac[..., c] = lut[rgb_idx[..., c], c if c < lut.shape[1] else 0]
    return dac
