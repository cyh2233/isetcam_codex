"""Achromatic optical transfer function models for the human eye."""

from __future__ import annotations

import numpy as np


def human_achromatic_otf(
    sample_sf: np.ndarray,
    model: str = "exp",
    pupil_d: float | None = None,
) -> np.ndarray:
    """Return achromatic optical transfer function for ``sample_sf``.

    Parameters
    ----------
    sample_sf : np.ndarray
        Spatial frequency vector in cycles/degree.
    model : {'exp', 'dl', 'watson'}, optional
        Model used for the calculation. Defaults to ``'exp'``.
    pupil_d : float, optional
        Pupil diameter in millimeters. Required for the ``'dl'`` and
        ``'watson'`` models.

    Returns
    -------
    np.ndarray
        Modulation transfer at each spatial frequency.
    """
    sample_sf = np.asarray(sample_sf, dtype=float)
    flag = model.lower()

    if flag in {"exp", "exponential"}:
        a = 0.1212
        w1 = 0.3481
        w2 = 0.6519
        return w1 * np.ones_like(sample_sf) + w2 * np.exp(-a * sample_sf)

    if flag in {"dl", "diffractionlimited"}:
        if pupil_d is None:
            raise ValueError("pupil diameter required")
        lam = 555.0
        u0 = pupil_d * np.pi * 1e6 / lam / 180.0
        u_hat = sample_sf / u0
        mtf = 2 / np.pi * (np.arccos(u_hat) - u_hat * np.sqrt(1 - u_hat ** 2))
        mtf[u_hat >= 1] = 0.0
        return mtf

    if flag == "watson":
        if pupil_d is None:
            raise ValueError("pupil diameter required")
        u1 = 21.95 - 5.512 * pupil_d + 0.3922 * pupil_d ** 2
        mtf_dl = human_achromatic_otf(sample_sf, "dl", pupil_d)
        return (1 + (sample_sf / u1) ** 2) ** (-0.62) * np.sqrt(mtf_dl)

    raise ValueError(f"Unknown model '{model}'")
