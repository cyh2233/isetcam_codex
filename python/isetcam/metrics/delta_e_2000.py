"""CIEDE2000 color difference."""

from __future__ import annotations

import numpy as np


def delta_e_2000(lab1: np.ndarray, lab2: np.ndarray) -> np.ndarray:
    """Return CIEDE2000 color difference between ``lab1`` and ``lab2``.

    Parameters
    ----------
    lab1, lab2 : np.ndarray
        Arrays of CIELAB values with final dimension of length 3.

    Returns
    -------
    np.ndarray
        Delta E values with the same shape as ``lab1`` without the last
        dimension.
    """
    lab1 = np.asarray(lab1, dtype=float)
    lab2 = np.asarray(lab2, dtype=float)
    if lab1.shape != lab2.shape:
        raise ValueError("lab1 and lab2 must have the same shape")

    L1, a1, b1 = lab1[..., 0], lab1[..., 1], lab1[..., 2]
    L2, a2, b2 = lab2[..., 0], lab2[..., 1], lab2[..., 2]

    C1 = np.sqrt(a1 ** 2 + b1 ** 2)
    C2 = np.sqrt(a2 ** 2 + b2 ** 2)
    C_bar = (C1 + C2) / 2

    G = 0.5 * (1 - np.sqrt((C_bar ** 7) / (C_bar ** 7 + 25 ** 7)))
    a1p = (1 + G) * a1
    a2p = (1 + G) * a2

    C1p = np.sqrt(a1p ** 2 + b1 ** 2)
    C2p = np.sqrt(a2p ** 2 + b2 ** 2)

    h1p = np.degrees(np.arctan2(b1, a1p)) % 360
    h2p = np.degrees(np.arctan2(b2, a2p)) % 360

    dLp = L2 - L1
    dCp = C2p - C1p

    dhp = h2p - h1p
    dhp = np.where(dhp > 180, dhp - 360, dhp)
    dhp = np.where(dhp < -180, dhp + 360, dhp)
    dhp = np.where((C1p * C2p) == 0, 0, dhp)

    dHp = 2 * np.sqrt(C1p * C2p) * np.sin(np.radians(dhp) / 2)

    Lp_bar = (L1 + L2) / 2
    Cp_bar = (C1p + C2p) / 2

    hp_bar = h1p + h2p
    hp_bar = np.where(np.abs(h1p - h2p) > 180, hp_bar + 360, hp_bar)
    hp_bar = np.where((C1p * C2p) == 0, h1p + h2p, hp_bar)
    hp_bar /= 2

    T = (
        1
        - 0.17 * np.cos(np.radians(hp_bar - 30))
        + 0.24 * np.cos(np.radians(2 * hp_bar))
        + 0.32 * np.cos(np.radians(3 * hp_bar + 6))
        - 0.2 * np.cos(np.radians(4 * hp_bar - 63))
    )

    dtheta = 30 * np.exp(-((hp_bar - 275) / 25) ** 2)
    Rc = 2 * np.sqrt((Cp_bar ** 7) / (Cp_bar ** 7 + 25 ** 7))

    Sl = 1 + (0.015 * ((Lp_bar - 50) ** 2)) / np.sqrt(20 + (Lp_bar - 50) ** 2)
    Sc = 1 + 0.045 * Cp_bar
    Sh = 1 + 0.015 * Cp_bar * T

    Rt = -Rc * np.sin(2 * np.radians(dtheta))

    dE = np.sqrt(
        (dLp / Sl) ** 2 + (dCp / Sc) ** 2 + (dHp / Sh) ** 2 + Rt * (dCp / Sc) * (dHp / Sh)  # noqa: E501
    )
    return dE

__all__ = ["delta_e_2000"]
