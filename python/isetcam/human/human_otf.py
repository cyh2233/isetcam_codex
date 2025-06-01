"""Human optical transfer function."""

from __future__ import annotations

import numpy as np
from scipy.interpolate import interp1d

from scipy.special import jn

from .human_achromatic_otf import human_achromatic_otf


_DEF_WAVE = np.arange(400, 701)


def _unit_frequency_list(n: int) -> np.ndarray:
    idx = np.arange(1, n + 1)
    mid = (n + 1) // 2 if n % 2 else n // 2 + 1
    c = idx - mid
    if c.max() == 0:
        return c.astype(float)
    return c / np.max(np.abs(c))


def _human_wave_defocus(wave: np.ndarray) -> np.ndarray:
    q1 = 1.7312
    q2 = 0.63346
    q3 = 0.21410
    return q1 - (q2 / (wave * 1e-3 - q3))




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


def _human_core(wave: np.ndarray, sample_sf: np.ndarray, p: float, d0: float) -> np.ndarray:  # noqa: E501
    D = _human_wave_defocus(wave)
    w20 = p ** 2 / 2 * (d0 * D) / (d0 + D)
    c = 1 / (np.tan(np.deg2rad(1)) * (1 / d0))
    ach_otf = human_achromatic_otf(sample_sf)
    s = np.zeros((wave.size, sample_sf.size))
    alpha = np.zeros_like(s)
    otf = np.zeros_like(s)
    lam = wave * 1e-9
    for ii in range(wave.size):
        s[ii, :] = (c * lam[ii] / (d0 * p)) * sample_sf
        alpha[ii, :] = ((4 * np.pi) / lam[ii]) * w20[ii] * s[ii, :]
        otf[ii, :] = _optics_defocused_mtf(s[ii, :], np.abs(alpha[ii, :]))
        otf[ii, :] *= ach_otf
    return otf


def human_otf(
    p_radius: float = 0.0015,
    d0: float = 59.9404,
    f_support: np.ndarray | None = None,
    wave: np.ndarray | None = None,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return human optical transfer function."""
    if wave is None:
        wave = _DEF_WAVE.copy()
    else:
        wave = np.asarray(wave, dtype=float)

    if f_support is None:
        max_f = 60
        f_list = _unit_frequency_list(max_f) * max_f
        X, Y = np.meshgrid(f_list, f_list)
        f_support = np.stack((X, Y), axis=2)

    dist = np.sqrt(f_support[:, :, 0] ** 2 + f_support[:, :, 1] ** 2)
    max_f1 = np.max(f_support[:, :, 0])
    max_f2 = np.max(f_support[:, :, 1])
    max_f = min(max_f1, max_f2)
    sample_sf = np.linspace(0, max_f, 40)

    otf = _human_core(wave, sample_sf, p_radius, d0)

    r, c = f_support.shape[:2]
    otf2d = np.zeros((r, c, wave.size))
    mask = dist > max_f

    for ii in range(wave.size):
        f = interp1d(sample_sf, otf[ii, :], kind="cubic", fill_value="extrapolate")
        tmp = np.abs(f(dist))
        tmp[mask] = 0.0
        otf2d[:, :, ii] = tmp

    return otf2d, f_support, wave
