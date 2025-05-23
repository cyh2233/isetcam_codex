"""Compute CIE XYZ tristimulus values from photon data."""

from __future__ import annotations

import numpy as np

from .quanta2energy import quanta_to_energy
from .ie_xyz_from_energy import ie_xyz_from_energy


def ie_xyz_from_photons(photons: np.ndarray, wavelength: np.ndarray) -> np.ndarray:
    """Convert spectral photon counts to CIE XYZ."""
    energy = quanta_to_energy(wavelength, photons)
    return ie_xyz_from_energy(energy, wavelength)
