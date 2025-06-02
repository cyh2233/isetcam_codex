# mypy: ignore-errors
"""Human eye defocus as a function of wavelength."""

from __future__ import annotations

import numpy as np

_DEF_WAVE = np.arange(400, 701)


def human_wave_defocus(wave: np.ndarray | None = None) -> np.ndarray:
    """Return human defocus in diopters for ``wave``.

    Parameters
    ----------
    wave : array-like, optional
        Wavelengths in nanometers. Defaults to ``400`` to ``700`` nm.

    Returns
    -------
    np.ndarray
        Defocus in diopters.
    """
    if wave is None:
        wave = _DEF_WAVE.copy()
    else:
        wave = np.asarray(wave, dtype=float)

    q1 = 1.7312
    q2 = 0.63346
    q3 = 0.21410
    return q1 - (q2 / (wave * 1e-3 - q3))
