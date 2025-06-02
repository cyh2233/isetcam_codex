# mypy: ignore-errors
"""Ijspeert model of the human MTF/PSF/LSF."""

from __future__ import annotations

import numpy as np


def ijspeert(
    age: float,
    pupil_diameter: float,
    pigmentation: float,
    q: np.ndarray,
    phi: np.ndarray | None = None,
) -> tuple[np.ndarray, np.ndarray | None, np.ndarray | None]:
    """Return MTF and optionally PSF/LSF from the Ijspeert model.

    Parameters
    ----------
    age : float
        Age of the observer in years.
    pupil_diameter : float
        Pupil diameter in millimeters.
    pigmentation : float
        Pigmentation parameter.
    q : np.ndarray
        Spatial frequencies in cycles/degree for the MTF.
    phi : np.ndarray, optional
        Angles in radians for the PSF/LSF computation.

    Returns
    -------
    tuple
        ``(MTF, PSF, LSF)``. ``PSF`` and ``LSF`` are ``None`` when ``phi`` is
        ``None``.
    """
    q = np.asarray(q, dtype=float).reshape(-1)

    D = 70.0
    AF = 1.0 + (age / D) ** 4

    c_sa = 1.0 / (1.0 + AF / (1.0 / pigmentation - 1.0))
    c_la = 1.0 / (1.0 + (1.0 / pigmentation - 1.0) / AF)

    b = 9000.0 - 936.0 * np.sqrt(AF)
    d = 3.2
    e = np.sqrt(AF) / 2000.0

    c1 = c_sa / (1.0 + (pupil_diameter / d) ** 2)
    c2 = c_sa / (1.0 + (d / pupil_diameter) ** 2)
    beta1 = (1.0 + (pupil_diameter / d) ** 2) / (b * pupil_diameter)
    beta2 = (1.0 + (d / pupil_diameter) ** 2) * (e - 1.0 / (b * pupil_diameter))

    c3 = c_la / ((1.0 + 25.0 * pigmentation) * (1.0 + 1.0 / AF))
    c4 = c_la - c3
    beta3 = 1.0 / (10.0 + 60.0 * pigmentation - 5.0 / AF)
    beta4 = 1.0

    c = np.array([c1, c2, c3, c4])
    beta = np.array([beta1, beta2, beta3, beta4])

    M_beta = np.exp(-360.0 * beta[:, None] * q[None, :])
    MTF = np.sum(c[:, None] * M_beta, axis=0)

    PSF = None
    LSF = None

    if phi is not None:
        phi = np.asarray(phi, dtype=float).reshape(-1)
        sinphi2 = np.sin(phi) ** 2
        cosphi2 = np.cos(phi) ** 2
        beta2_vec = beta ** 2

        f_beta = np.zeros((4, phi.size))
        for i in range(4):
            f_beta[i, :] = beta[i] / (
                2 * np.pi * (sinphi2 + beta2_vec[i] * cosphi2) ** 1.5
            )
        PSF = np.sum(c[:, None] * f_beta, axis=0)

        l_beta = np.zeros((4, phi.size))
        for i in range(4):
            l_beta[i, :] = beta[i] / (
                np.pi * (sinphi2 + beta2_vec[i] * cosphi2)
            )
        LSF = np.sum(c[:, None] * l_beta, axis=0)

    return MTF, PSF, LSF
