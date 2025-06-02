# mypy: ignore-errors
"""Human line spread function."""

from __future__ import annotations

import numpy as np
from scipy.fft import fftshift, ifft

from .human_otf import human_otf, _unit_frequency_list

_DEF_WAVE = np.arange(400, 701)


def human_lsf(
    pupil_radius: float = 0.0015,
    dioptric_power: float = 59.9404,
    unit: str = "mm",
    wave: np.ndarray | None = None,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return human line spread function."""
    if wave is None:
        wave = _DEF_WAVE.copy()
    else:
        wave = np.asarray(wave, dtype=float)

    otf2d, f_support, wave = human_otf(pupil_radius, dioptric_power, None, wave)

    n_wave = wave.size
    n_samples = otf2d.shape[0]
    line_spread = np.zeros((n_wave, n_samples))

    for ii in range(n_wave):
        tmp = otf2d[:, :, ii]
        center = tmp[:, 0]
        this_lsf = fftshift(np.abs(ifft(center)))
        line_spread[ii, :] = this_lsf

    delta_space = 1 / (2 * np.max(f_support))
    spatial_extent_deg = delta_space * n_samples
    f_list = _unit_frequency_list(n_samples)
    x_dim = f_list * spatial_extent_deg

    mm_per_deg = 0.330
    unit_l = unit.lower()
    if unit_l in {"mm", "default"}:
        x_dim = x_dim * mm_per_deg
    elif unit_l == "um":
        x_dim = x_dim * mm_per_deg * 1e3
    else:
        raise ValueError(f"Unknown unit {unit}")

    return line_spread, x_dim, wave
