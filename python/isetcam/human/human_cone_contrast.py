"""Cone contrast for a signal relative to a background."""

from __future__ import annotations

import numpy as np
from ..ie_read_spectra import ie_read_spectra
from ..iset_root_path import iset_root_path
from ..quanta2energy import quanta_to_energy

Units = "energy", "photons", "quanta"

def human_cone_contrast(
    spd_signal: np.ndarray,
    spd_background: np.ndarray,
    wave: np.ndarray,
    units: str = "energy",
) -> np.ndarray:
    """Return L, M, S cone contrast of ``spd_signal`` on ``spd_background``.

    Parameters
    ----------
    spd_signal : np.ndarray
        Signal spectral power distribution. Columns represent different
        signals and the length of the first dimension must match ``wave``.
    spd_background : np.ndarray
        Background spectral power distribution with length ``wave``.
    wave : np.ndarray
        Wavelength samples in nanometers.
    units : {'energy', 'photons', 'quanta'}, optional
        Units of the input spectra. Defaults to ``'energy'``.

    Returns
    -------
    np.ndarray
        Cone contrast matrix with shape ``(3, n)`` where ``n`` is the number
        of signal spectra.
    """
    spd_signal = np.asarray(spd_signal, dtype=float)
    spd_background = np.asarray(spd_background, dtype=float).reshape(-1)
    wave = np.asarray(wave, dtype=float).reshape(-1)

    if spd_signal.shape[0] != wave.size or spd_background.size != wave.size:
        raise ValueError("wave length must match spd dimensions")

    if units.lower() in {"photons", "quanta"}:
        spd_signal = quanta_to_energy(wave, spd_signal)
        spd_background = quanta_to_energy(wave, spd_background)

    root = iset_root_path()
    cone_file = root / "data" / "human" / "stockman.mat"
    cones, _, _, _ = ie_read_spectra(cone_file, wave)

    back_cones = cones.T @ spd_background
    sig_cones = cones.T @ spd_signal

    return np.diag(1.0 / back_cones) @ sig_cones
