# mypy: ignore-errors
"""Create a simple :class:`OpticalImage` with uniform photons."""

from __future__ import annotations

from typing import Optional

import numpy as np

from .oi_class import OpticalImage


_DEF_SIZE = 128
_DEF_WAVE = np.arange(400, 701, 10, dtype=float)


def oi_create(
    name: Optional[str] = None,
    size: int = _DEF_SIZE,
    wave: Optional[np.ndarray] = None,
) -> OpticalImage:
    """Return a uniform :class:`OpticalImage`.

    Parameters
    ----------
    name:
        Optional name for the optical image.
    size:
        Spatial dimension in pixels for the square photon data.
    wave:
        Optional wavelength samples. Defaults to 400--700 nm in 10 nm steps.
    """
    if size <= 0:
        raise ValueError("size must be positive")

    if wave is None:
        wave_arr = _DEF_WAVE
    else:
        wave_arr = np.asarray(wave, dtype=float).reshape(-1)

    photons = np.ones((size, size, wave_arr.size), dtype=float)
    return OpticalImage(photons=photons, wave=wave_arr, name=name)


__all__ = ["oi_create"]
