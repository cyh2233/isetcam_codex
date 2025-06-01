from __future__ import annotations

import numpy as np
from scipy.special import jn

from .optics_class import Optics


def optics_defocused_mtf(s: np.ndarray, alpha: np.ndarray) -> np.ndarray:
    """Diffraction-limited MTF with defocus.

    Parameters
    ----------
    s : array-like
        Reduced spatial frequency in the range ``0`` to ``2``.
    alpha : array-like
        Defocus parameter ``w20`` scaled by frequency.

    Returns
    -------
    np.ndarray
        Modulation transfer values for each spatial frequency.
    """
    s = np.asarray(s, dtype=float)
    alpha = np.asarray(alpha, dtype=float)
    nf = np.abs(s) / 2.0
    beta = np.sqrt(1.0 - nf ** 2)
    otf = np.zeros_like(nf)
    ii = alpha == 0
    if np.any(ii):
        otf[ii] = (2.0 / np.pi) * (np.arccos(nf[ii]) - nf[ii] * beta[ii])
    jj = ~ii
    if np.any(jj):
        H1 = (
            beta[jj] * jn(1, alpha[jj])
            + 0.5 * np.sin(2 * beta[jj]) * (jn(1, alpha[jj]) - jn(3, alpha[jj]))
            - 0.25 * np.sin(4 * beta[jj]) * (jn(3, alpha[jj]) - jn(5, alpha[jj]))
        )
        H2 = (
            np.sin(beta[jj]) * (jn(0, alpha[jj]) - jn(2, alpha[jj]))
            + (1.0 / 3.0)
            * np.sin(3 * beta[jj])
            * (jn(2, alpha[jj]) - jn(4, alpha[jj]))
            - (1.0 / 5.0)
            * np.sin(5 * beta[jj])
            * (jn(4, alpha[jj]) - jn(6, alpha[jj]))
        )
        otf[jj] = (
            (4.0 / (np.pi * alpha[jj])) * np.cos(alpha[jj] * nf[jj]) * H1
            - (4.0 / (np.pi * alpha[jj])) * np.sin(alpha[jj] * nf[jj]) * H2
        )
    if otf.size > 0 and otf.flat[0] != 0:
        otf = otf / otf.flat[0]
    return otf


def optics_defocus_core(
    optics: Optics,
    sample_sf: np.ndarray,
    D: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Compute defocused OTF for ``optics``.

    Parameters
    ----------
    optics : Optics
        Optics description.
    sample_sf : array-like
        Spatial frequencies in cycles/degree.
    D : array-like
        Defocus in diopters for each wavelength.

    Returns
    -------
    tuple[np.ndarray, np.ndarray]
        ``(otf, sample_sf_mm)`` where ``otf`` has shape ``(n_wave, n_sf)`` and
        ``sample_sf_mm`` are the frequencies in cycles/mm.
    """
    if optics is None:
        raise ValueError("optics is required")

    sample_sf = np.asarray(sample_sf, dtype=float).reshape(-1)
    D = np.asarray(D, dtype=float).reshape(-1)
    p = optics.f_length / (2.0 * optics.f_number)
    D0 = 1.0 / optics.f_length

    w20 = (p ** 2 / 2.0) * (D0 * D) / (D0 + D)
    c = D0 / np.tan(np.deg2rad(1.0))

    cSF = sample_sf * c
    ii = cSF == 0
    if np.any(ii):
        nonzero = cSF[~ii]
        if nonzero.size == 0:
            cSF[ii] = 1e-12
        else:
            cSF[ii] = np.min(nonzero) * 1e-12

    wave = np.asarray(optics.wave, dtype=float) * 1e-9
    s = np.zeros((wave.size, sample_sf.size))
    alpha = np.zeros_like(s)
    otf = np.zeros_like(s)

    for i in range(wave.size):
        s[i, :] = (wave[i] / (D0 * p)) * cSF
        alpha[i, :] = (4.0 * np.pi / wave[i]) * w20[i] * np.abs(s[i, :])
        otf[i, :] = optics_defocused_mtf(s[i, :], np.abs(alpha[i, :]))

    l = np.angle(otf) != 0
    otf[l] = 0
    otf = np.real(otf)

    deg_per_mm = 1.0 / (np.tan(np.deg2rad(1.0)) * (1.0 / D0) * 1000.0)
    sample_sf_mm = sample_sf * deg_per_mm

    return otf, sample_sf_mm
