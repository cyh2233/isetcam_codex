# mypy: ignore-errors
"""Compute lens exposure value (EV)."""

from __future__ import annotations

import numpy as np


def exposure_value(f_number: float, exposure_time: float) -> float:
    """Return the exposure value for a given aperture and shutter speed.

    Parameters
    ----------
    f_number : float
        Lens F-number.
    exposure_time : float
        Exposure time in seconds.

    Returns
    -------
    float
        Exposure value defined as ``log2(f_number**2 / exposure_time)``.
    """
    f_number = float(f_number)
    exposure_time = float(exposure_time)
    if f_number <= 0 or exposure_time <= 0:
        raise ValueError("f_number and exposure_time must be positive")

    return float(np.log2(f_number ** 2 / exposure_time))


__all__ = ["exposure_value"]
