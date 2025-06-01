"""Evaluate photobiological safety of ultraviolet and blue light."""

from __future__ import annotations

from typing import Tuple
import numpy as np

from ..data_path import data_path
from ..ie_read_spectra import ie_read_spectra


_DEF_METHOD = "eye"


def human_uv_safety(
    energy: np.ndarray,
    wave: np.ndarray,
    method: str = _DEF_METHOD,
    duration: float = 1.0,
) -> Tuple[float, float, bool | None]:
    """Return safety metrics for spectral ``energy``.

    Parameters
    ----------
    energy : np.ndarray
        Spectral irradiance or radiance in watts/(nm m^2).
    wave : np.ndarray
        Wavelength samples in nanometers.
    method : str, optional
        One of ``'skineye'``, ``'eye'``, ``'bluehazard'``,
        ``'thermalskin'``, or ``'skinthermalthreshold'``.
        Defaults to ``'eye'``.
    duration : float, optional
        Exposure duration in seconds. Defaults to 1.0.

    Returns
    -------
    tuple
        ``(val, level, safety)`` as defined by the IEC 62471 standard.
    """
    energy = np.asarray(energy, dtype=float).reshape(-1)
    wave = np.asarray(wave, dtype=float).reshape(-1)
    if energy.size != wave.size:
        raise ValueError("energy and wave must have the same length")

    if wave.size > 1:
        d_lambda = float(wave[1] - wave[0])
    else:
        d_lambda = 10.0

    m = method.lower()
    val: float | bool
    level: float
    safety: bool | None = None

    if m == "skineye":
        actinic, _, _, _ = ie_read_spectra(
            data_path("safetyStandards/Actinic.mat"), wave
        )
        mask = wave <= 400
        level = float(np.dot(actinic[mask], energy[mask]) * d_lambda)
        val = (30.0 / level) / 60.0
    elif m == "eye":
        mask = wave <= 400
        level = float(np.sum(energy[mask]) * d_lambda)
        if duration <= 1000:
            safety = level * duration < 10000
        else:
            safety = level < 10
        val = safety
    elif m == "bluehazard":
        blue, _, _, _ = ie_read_spectra(
            data_path("safetyStandards/blueLightHazard.mat"), wave
        )
        level = float(np.dot(blue, energy) * d_lambda)
        if duration <= 1e4 and level * duration < 1e6:
            safety = True
        elif duration > 1e4 and level < 100:
            safety = True
        else:
            safety = False
        if level > 100:
            if duration <= 1e4:
                val = 1e6 / level / 60.0
            else:
                val = 0.0
            # when level <= 100 the standard does not specify a limit
        else:
            val = float("inf")
    elif m == "thermalskin":
        level = float(duration ** 0.25 * np.sum(energy) * d_lambda)
        val = level
        safety = duration <= 10 and level < 20000 * duration ** 0.25
    elif m == "skinthermalthreshold":
        if wave.size > 1:
            d = float(wave[1] - wave[0])
        else:
            d = 10.0
        val = float(np.sum(energy) * d * duration)
        level = val
        h = 2 * duration ** 0.25 * 1e4
        safety = val < h
    else:
        raise ValueError(f"Unknown method '{method}'")

    return val, level, safety
