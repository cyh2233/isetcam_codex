# mypy: ignore-errors
"""Utilities for extracting pixel spectra from a :class:`Scene`."""

from __future__ import annotations

import numpy as np

from .scene_class import Scene
from ..quanta2energy import quanta_to_energy


def scene_photons_from_vector(scene: Scene, row: int, col: int) -> np.ndarray:
    """Return photons at ``(row, col)`` as a 1-D vector."""
    photons = np.asarray(scene.photons)
    if photons.ndim != 3:
        raise ValueError("scene.photons must be a 3-D array")
    h, w, _ = photons.shape
    if row < 0 or row >= h or col < 0 or col >= w:
        raise ValueError("row/col index out of bounds")
    return photons[row, col, :].reshape(-1)


def scene_energy_from_vector(scene: Scene, row: int, col: int) -> np.ndarray:
    """Return spectral energy at ``(row, col)`` as a 1-D vector."""
    photons_vec = scene_photons_from_vector(scene, row, col)
    energy = quanta_to_energy(scene.wave, photons_vec)
    return energy.reshape(-1)


__all__ = ["scene_photons_from_vector", "scene_energy_from_vector"]
