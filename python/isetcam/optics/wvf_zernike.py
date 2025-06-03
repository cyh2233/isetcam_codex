# mypy: ignore-errors
"""Evaluate a wavefront from Zernike coefficients."""

from __future__ import annotations

import numpy as np
from math import factorial

# Mapping for the first 10 Noll indices to (n, m)
_NOLL_TO_NM = {
    1: (0, 0),
    2: (1, -1),
    3: (1, 1),
    4: (2, 0),
    5: (2, -2),
    6: (2, 2),
    7: (3, -1),
    8: (3, 1),
    9: (3, -3),
    10: (3, 3),
}


def _zernike(n: int, m: int, rho: np.ndarray, theta: np.ndarray) -> np.ndarray:
    m_abs = abs(m)
    out = np.zeros_like(rho, dtype=float)
    for k in range((n - m_abs) // 2 + 1):
        c = (
            (-1) ** k
            * factorial(n - k)
            / (factorial(k) * factorial((n + m_abs) // 2 - k) * factorial((n - m_abs) // 2 - k))
        )
        out += c * rho ** (n - 2 * k)
    if m >= 0:
        return out * np.cos(m * theta)
    else:
        return out * np.sin(m_abs * theta)


def wvf_zernike(coeffs: np.ndarray, rho: np.ndarray, theta: np.ndarray) -> np.ndarray:
    """Return wavefront from ``coeffs`` evaluated on the ``(rho, theta)`` grid."""
    if coeffs.ndim != 1:
        raise ValueError("coeffs must be 1-D")
    wvf = np.zeros_like(rho, dtype=float)
    for j, c in enumerate(coeffs, start=1):
        if j not in _NOLL_TO_NM:
            raise ValueError("Noll index %d not supported" % j)
        n, m = _NOLL_TO_NM[j]
        wvf += c * _zernike(n, m, rho, theta)
    return wvf


__all__ = ["wvf_zernike"]
