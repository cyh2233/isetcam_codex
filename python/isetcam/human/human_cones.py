# mypy: ignore-errors
"""Spectral cone fundamentals corrected for macular pigment."""

from __future__ import annotations

import numpy as np
from scipy.io import loadmat

from ..ie_read_spectra import ie_read_spectra
from ..data_path import data_path


_DEF_WAVE = np.arange(370, 731)


def _macular_unit_density(wave: np.ndarray) -> np.ndarray:
    """Return unit macular pigment density at ``wave``."""
    mat = loadmat(data_path("human/macularPigment.mat"))
    src_wave = mat["wavelength"].ravel()
    data = mat["data"].ravel()
    return np.interp(wave, src_wave, data, left=0.0, right=0.0) / 0.3521


def human_cones(
    file_name: str = "stockmanAbs",
    wave: np.ndarray | None = None,
    macular_density: float | None = None,
    included_density: float = 0.35,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return cone spectral sensitivities corrected for macular pigment."""
    if wave is None:
        wave = _DEF_WAVE.copy()
    else:
        wave = np.asarray(wave, dtype=float)

    fname = file_name
    if not fname.endswith(".mat"):
        fname = f"{fname}.mat"
    path = data_path(f"human/{fname}")
    cones, wave, _, _ = ie_read_spectra(path, wave)

    if macular_density is None:
        macular_correction = np.ones(wave.shape)
        return cones, macular_correction, wave

    unit = _macular_unit_density(wave)
    macular_correction = 10.0 ** (-(unit * (macular_density - included_density)))
    cones = cones * macular_correction[:, None]
    return cones, macular_correction, wave
