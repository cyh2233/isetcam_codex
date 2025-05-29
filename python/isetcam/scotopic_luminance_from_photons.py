"""Calculate scotopic luminance from photon counts."""

from __future__ import annotations

import numpy as np

from .quanta2energy import quanta_to_energy
from .scotopic_luminance_from_energy import scotopic_luminance_from_energy


def scotopic_luminance_from_photons(
    photons: np.ndarray, wavelength: np.ndarray, binwidth: float | None = None
) -> np.ndarray:
    """Compute scotopic luminance (cd/m^2) from spectral photon data."""
    energy = quanta_to_energy(wavelength, photons)
    return scotopic_luminance_from_energy(energy, wavelength, binwidth)
