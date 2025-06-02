# mypy: ignore-errors
from __future__ import annotations

import numpy as np


def _cpiq_csf(v: np.ndarray) -> np.ndarray:
    a = 75.0
    b = 0.2
    c = 0.8
    K = 34.05
    csf = a * (v ** c) * np.exp(-b * v) / K
    if csf.size:
        csf = csf / csf.max()
    return csf


def iso_acutance(cpd: np.ndarray, lum_mtf: np.ndarray) -> float:
    cpd = np.asarray(cpd, dtype=float)
    lum_mtf = np.asarray(lum_mtf, dtype=float)
    if cpd.shape != lum_mtf.shape:
        raise ValueError("cpd and lum_mtf must have the same shape")
    if cpd.size < 2:
        return float(np.sum(lum_mtf))
    cpiq = _cpiq_csf(cpd)
    dv = float(cpd[1] - cpd[0])
    A = np.sum(lum_mtf * cpiq) * dv
    Ar = np.sum(cpiq) * dv
    return float(A / Ar)


__all__ = ["iso_acutance"]
