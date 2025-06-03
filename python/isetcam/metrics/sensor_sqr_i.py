# mypy: ignore-errors
"""Barten's Square Root Integral metric.

This is a Python reimplementation of the MATLAB ``ieSQRI`` function
found in ``metrics/sqri/ieSQRI.m``. The metric predicts perceived
image quality based on the display MTF and luminance.
"""

from __future__ import annotations

import numpy as np
from typing import Sequence, Tuple


def sensor_sqr_i(
    sf: Sequence[float] | np.ndarray,
    d_mtf: Sequence[float] | np.ndarray,
    luminance: float,
    *,
    width: float = 40.0,
) -> Tuple[float, np.ndarray]:
    """Return the SQRI value and human CSF.

    Parameters
    ----------
    sf : sequence of float
        Spatial frequency samples in cycles per degree.
    d_mtf : sequence of float
        Display MTF sampled at ``sf``.
    luminance : float
        Display luminance in ``cd/m^2``.
    width : float, optional
        Angular width of the display in degrees. Default is ``40``.

    Returns
    -------
    tuple of float and ndarray
        ``(sqri, h_csf)`` where ``h_csf`` is the human contrast
        sensitivity function sampled at ``sf``.
    """

    sf = np.asarray(sf, dtype=float).reshape(-1)
    d_mtf = np.asarray(d_mtf, dtype=float).reshape(-1)
    if sf.shape != d_mtf.shape:
        raise ValueError("sf and d_mtf must have the same shape")

    a = 540 * (1 + (0.7 / luminance)) ** (-0.2) / (
        1 + (12 / (width * (1 + (sf / 3) ** 2)))
    )
    b = 0.3 * (1 + (100 / luminance)) ** 0.15
    c = 0.06

    h_csf = (a * sf) * np.exp(-b * sf) * np.sqrt(1 + c * np.exp(b * sf))
    h_csf = h_csf.reshape(-1)

    du = np.diff(sf)
    u = sf[1:]
    dm = 0.5 * (d_mtf[:-1] + d_mtf[1:])
    dh = 0.5 * (h_csf[:-1] + h_csf[1:])

    sqri = float((1 / np.log(2)) * np.sum((dm * dh) ** 0.5 * (du / u)))

    return sqri, h_csf


__all__ = ["sensor_sqr_i"]
