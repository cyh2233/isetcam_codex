# mypy: ignore-errors
"""Generate a blackbody spectral distribution."""

from __future__ import annotations

import numpy as np

from ..vc_constants import vc_constants


def illuminant_blackbody(temp: float, wave: np.ndarray) -> np.ndarray:
    """Return blackbody spectral radiance at ``temp`` for wavelengths ``wave``."""
    wave = np.asarray(wave, dtype=float)
    h = vc_constants("h")
    c = vc_constants("c")
    k = vc_constants("j")
    lam = wave * 1e-9
    exponent = (h * c) / (lam * k * temp)
    spd = (2 * h * c**2) / (lam**5) / (np.exp(exponent) - 1)
    return spd
