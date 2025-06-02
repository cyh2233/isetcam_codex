# mypy: ignore-errors
"""Accessor utilities for :class:`Scene`."""

from __future__ import annotations

import numpy as np

from .scene_class import Scene


def get_photons(scene: Scene) -> np.ndarray:
    """Return the photon data from ``scene``."""
    return scene.photons


def set_photons(scene: Scene, photons: np.ndarray) -> None:
    """Set the photon data for ``scene``."""
    scene.photons = np.asarray(photons)


def get_n_wave(scene: Scene) -> int:
    """Return the number of wavelength samples in ``scene``."""
    return len(scene.wave)
