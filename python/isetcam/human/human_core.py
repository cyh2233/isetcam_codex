"""Core modulation transfer for human optics."""

from __future__ import annotations

import numpy as np
from scipy.special import jn

from .human_wave_defocus import human_wave_defocus
from .human_achromatic_otf import human_achromatic_otf

_DEF_WAVE = np.arange(400, 701)


def _optics_defocused_mtf(s: np.ndarray, alpha: np.ndarray) -> np.ndarray:
    nf = np.abs(s) / 2.0
    beta = np.sqrt(1.0 - nf ** 2)
    otf = np.zeros_like(nf)
    ii = alpha == 0
    if np.any(ii):
        otf[ii] = (2 / np.pi) * (np.arccos(nf[ii]) - nf[ii] * beta[ii])
    jj = ~ii
    if np.any(jj):
        H1 = (
            beta[jj] * jn(1, alpha[jj])
            + 0.5 * np.sin(2 * beta[jj]) * (jn(1, alpha[jj]) - jn(3, alpha[jj]))
            - 0.25 * np.sin(4 * beta[jj]) * (jn(3, alpha[jj]) - jn(5, alpha[jj]))
        )
        H2 = (
            np.sin(beta[jj]) * (jn(0, alpha[jj]) - jn(2, alpha[jj]))
            + (1 / 3) * np.sin(3 * beta[jj]) * (jn(2, alpha[jj]) - jn(4, alpha[jj]))
            - (1 / 5) * np.sin(5 * beta[jj]) * (jn(4, alpha[jj]) - jn(6, alpha[jj]))
        )
        otf[jj] = (
            (4 / (np.pi * alpha[jj])) * np.cos(alpha[jj] * nf[jj]) * H1
            - (4 / (np.pi * alpha[jj])) * np.sin(alpha[jj] * nf[jj]) * H2
        )
    if otf[0] != 0:
        otf = otf / otf[0]
    return otf


def human_core(
    sample_sf: np.ndarray,
    pupil_radius: float = 0.0015,
    dioptric_power: float = 59.9404,
    wave: np.ndarray | None = None,
) -> np.ndarray:
    """Return base OTF values for ``sample_sf`` across ``wave``."""
    if wave is None:
        wave = _DEF_WAVE.copy()
    else:
        wave = np.asarray(wave, dtype=float)
    sample_sf = np.asarray(sample_sf, dtype=float)

    D = human_wave_defocus(wave)
    w20 = pupil_radius ** 2 / 2 * (dioptric_power * D) / (dioptric_power + D)
    c = 1 / (np.tan(np.deg2rad(1)) * (1 / dioptric_power))
    ach_otf = human_achromatic_otf(sample_sf)

    s = np.zeros((wave.size, sample_sf.size))
    alpha = np.zeros_like(s)
    otf = np.zeros_like(s)
    lam = wave * 1e-9

    for ii in range(wave.size):
        s[ii, :] = (c * lam[ii] / (dioptric_power * pupil_radius)) * sample_sf
        alpha[ii, :] = ((4 * np.pi) / lam[ii]) * w20[ii] * s[ii, :]
        otf[ii, :] = _optics_defocused_mtf(s[ii, :], np.abs(alpha[ii, :]))
        otf[ii, :] *= ach_otf

    return otf
