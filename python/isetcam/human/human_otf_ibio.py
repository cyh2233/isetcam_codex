# mypy: ignore-errors
"""Human optical transfer function from ISETBio (ifftshifted)."""

from __future__ import annotations

import numpy as np
from scipy.interpolate import interp1d

from .human_core import human_core as _human_core
from .human_otf import _unit_frequency_list

_DEF_WAVE = np.arange(400, 701)


def human_otf_ibio(
    p_radius: float = 0.0015,
    d0: float = 58.8235,
    f_support: np.ndarray | None = None,
    wave: np.ndarray | None = None,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return human OTF with DC at [0,0] via ``ifftshift``.

    Parameters
    ----------
    p_radius : float, optional
        Pupil radius in meters. Defaults to ``0.0015`` (3 mm diameter).
    d0 : float, optional
        Dioptric power of the eye. Defaults to ``58.8235``.
    f_support : np.ndarray, optional
        Frequency support matrix in cycles/degree. When ``None`` a grid
        covering ``[-60, 60]`` is used.
    wave : np.ndarray, optional
        Wavelength samples in nanometers. Defaults to ``400:700``.

    Returns
    -------
    tuple[np.ndarray, np.ndarray, np.ndarray]
        ``(otf2d, f_support, wave)`` where ``otf2d`` has shape ``(N, N, len(wave))``.
    """
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
    max_f = float(min(max_f1, max_f2))
    sample_sf = np.linspace(0, max_f, 40)

    otf = _human_core(sample_sf, p_radius, d0, wave)

    r, c = f_support.shape[:2]
    otf2d = np.zeros((r, c, wave.size))
    mask = dist > max_f

    for ii in range(wave.size):
        f = interp1d(sample_sf, otf[ii, :], kind="cubic", fill_value="extrapolate")
        tmp = np.abs(f(dist))
        tmp[mask] = 0.0
        otf2d[:, :, ii] = np.fft.ifftshift(tmp)

    return otf2d, f_support, wave
