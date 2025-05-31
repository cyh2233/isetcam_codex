"""CIE94 color difference."""

from __future__ import annotations

import numpy as np


def delta_e_94(lab1: np.ndarray, lab2: np.ndarray, k: tuple[float, float, float] | np.ndarray = (1.0, 1.0, 1.0)) -> np.ndarray:  # noqa: E501
    """Return CIE94 color difference between ``lab1`` and ``lab2``.

    Parameters
    ----------
    lab1, lab2 : np.ndarray
        Arrays of CIELAB values with final dimension 3.
    k : sequence of float, optional
        Parametric weighting factors ``(kL, kC, kH)``.

    Returns
    -------
    np.ndarray
        Delta E values.
    """
    lab1 = np.asarray(lab1, dtype=float)
    lab2 = np.asarray(lab2, dtype=float)
    if lab1.shape != lab2.shape:
        raise ValueError("lab1 and lab2 must have the same shape")
    k = np.asarray(k, dtype=float).reshape(3)

    L1, a1, b1 = lab1[..., 0], lab1[..., 1], lab1[..., 2]
    L2, a2, b2 = lab2[..., 0], lab2[..., 1], lab2[..., 2]

    Cab1 = np.sqrt(a1 ** 2 + b1 ** 2)
    Cab2 = np.sqrt(a2 ** 2 + b2 ** 2)
    deltaL = L1 - L2
    deltaC = Cab1 - Cab2

    diff = lab1 - lab2
    deltaE = np.sqrt(np.sum(diff ** 2, axis=-1))
    deltaH = np.sqrt(np.maximum(deltaE ** 2 - deltaL ** 2 - deltaC ** 2, 0))

    sL = 1.0
    sC = 1.0 + 0.045 * Cab1
    sH = 1.0 + 0.015 * Cab1

    eL = deltaL / (sL * k[0])
    eC = deltaC / (sC * k[1])
    eH = deltaH / (sH * k[2])

    de94 = np.sqrt(eL ** 2 + eC ** 2 + eH ** 2)
    return de94

__all__ = ["delta_e_94"]
