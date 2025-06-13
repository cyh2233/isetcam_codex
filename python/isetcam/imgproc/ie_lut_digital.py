# mypy: ignore-errors
"""Convert DAC values to linear RGB intensities using a gamma table."""

from __future__ import annotations

import numpy as np
from typing import Union


def ie_lut_digital(dac: np.ndarray, g_table: Union[np.ndarray, float] = 2.2) -> np.ndarray:
    """Return linear RGB values computed from ``dac`` through ``g_table``.

    Parameters
    ----------
    dac : np.ndarray
        Digital values. Can be 2-D or 3-D. Values must be integers in the
        range ``[0, n_levels-1]`` where ``n_levels`` is the length of
        ``g_table``.
    g_table : Union[np.ndarray, float], optional
        Gamma table mapping DAC values to linear intensity. If scalar,
        ``dac`` values are raised to this power. Defaults to ``2.2``.

    Returns
    -------
    np.ndarray
        Linear intensity values in ``float``.
    """

    dac = np.asarray(dac)
    if np.isscalar(g_table):
        return dac.astype(float) ** float(g_table)

    lut = np.asarray(g_table, dtype=float)
    if lut.ndim == 1:
        lut = lut[:, np.newaxis]
    n_levels = lut.shape[0]

    if dac.max() >= n_levels:
        raise ValueError("DAC value exceeds gamma table length")

    if lut.shape[1] == 1 and dac.ndim == 3:
        lut = np.tile(lut, (1, dac.shape[2]))

    if dac.ndim == 2:
        dac_idx = dac.astype(int)
        return lut[dac_idx, 0]

    rgb = np.empty_like(dac, dtype=float)
    for c in range(dac.shape[2]):
        rgb[..., c] = lut[dac[..., c].astype(int), c if c < lut.shape[1] else 0]
    return rgb
