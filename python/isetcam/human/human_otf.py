# mypy: ignore-errors
"""Human optical transfer function."""

from __future__ import annotations

import numpy as np
from scipy.interpolate import interp1d

from .human_wave_defocus import human_wave_defocus as _human_wave_defocus
from .human_core import human_core as _human_core


_DEF_WAVE = np.arange(400, 701)


def _unit_frequency_list(n: int) -> np.ndarray:
    idx = np.arange(1, n + 1)
    mid = (n + 1) // 2 if n % 2 else n // 2 + 1
    c = idx - mid
    if c.max() == 0:
        return c.astype(float)
    return c / np.max(np.abs(c))




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

    otf = _human_core(sample_sf, p_radius, d0, wave)

    r, c = f_support.shape[:2]
    otf2d = np.zeros((r, c, wave.size))
    mask = dist > max_f

    for ii in range(wave.size):
        f = interp1d(sample_sf, otf[ii, :], kind="cubic", fill_value="extrapolate")
        tmp = np.abs(f(dist))
        tmp[mask] = 0.0
        otf2d[:, :, ii] = tmp

    return otf2d, f_support, wave
