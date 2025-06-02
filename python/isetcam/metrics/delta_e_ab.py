# mypy: ignore-errors
"""Wrapper for various CIELAB color difference metrics."""

from __future__ import annotations

import numpy as np

from .delta_e_2000 import delta_e_2000
from .delta_e_94 import delta_e_94


def delta_e_ab(lab1: np.ndarray, lab2: np.ndarray, version: str = "2000") -> np.ndarray:
    """Return CIELAB color difference between ``lab1`` and ``lab2``.

    Parameters
    ----------
    lab1, lab2 : np.ndarray
        Arrays of CIELAB values with final dimension 3.
    version : str, optional
        Which DeltaE formula to use. Supported values are ``"2000"``,
        ``"1994"`` and ``"1976"``. The default is ``"2000"``.

    Returns
    -------
    np.ndarray
        Delta E values.
    """
    lab1 = np.asarray(lab1, dtype=float)
    lab2 = np.asarray(lab2, dtype=float)
    if lab1.shape != lab2.shape:
        raise ValueError("lab1 and lab2 must have the same shape")

    v = version.lower()
    if v in {"2000", "de2000", "ciede2000"}:
        return delta_e_2000(lab1, lab2)
    elif v in {"1994", "94"}:
        return delta_e_94(lab1, lab2)
    elif v in {"1976", "lab", "76"}:
        diff = lab1 - lab2
        return np.sqrt(np.sum(diff ** 2, axis=-1))
    else:
        raise ValueError(f"Unsupported deltaE version: {version}")

__all__ = ["delta_e_ab"]
