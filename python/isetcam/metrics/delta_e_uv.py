"""CIELUV color difference."""

from __future__ import annotations

import numpy as np


def delta_e_uv(luv1: np.ndarray, luv2: np.ndarray) -> np.ndarray:
    """Return CIELUV color difference between ``luv1`` and ``luv2``.

    Parameters
    ----------
    luv1, luv2 : np.ndarray
        Arrays of CIELUV values with final dimension 3.

    Returns
    -------
    np.ndarray
        Delta E values.
    """
    luv1 = np.asarray(luv1, dtype=float)
    luv2 = np.asarray(luv2, dtype=float)
    if luv1.shape != luv2.shape:
        raise ValueError("luv1 and luv2 must have the same shape")

    diff = luv1 - luv2
    de = np.sqrt(np.sum(diff ** 2, axis=-1))
    return de

__all__ = ["delta_e_uv"]
