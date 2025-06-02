# mypy: ignore-errors
"""Accessor utilities for :class:`OpticalImage`."""

from __future__ import annotations

import numpy as np

from .oi_class import OpticalImage


def get_photons(oi: OpticalImage) -> np.ndarray:
    """Return the irradiance data from ``oi``."""
    return oi.photons


def set_photons(oi: OpticalImage, photons: np.ndarray) -> None:
    """Set the irradiance data for ``oi``."""
    oi.photons = np.asarray(photons)


def get_n_wave(oi: OpticalImage) -> int:
    """Return the number of wavelength samples in ``oi``."""
    return len(oi.wave)
