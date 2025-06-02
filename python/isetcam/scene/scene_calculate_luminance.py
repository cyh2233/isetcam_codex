# mypy: ignore-errors
"""Calculate scene luminance from photon data."""

from __future__ import annotations

import numpy as np

from .scene_class import Scene
from ..luminance_from_photons import luminance_from_photons


def scene_calculate_luminance(scene: Scene) -> tuple[np.ndarray, float]:
    """Return per-pixel and mean luminance for ``scene``.

    Parameters
    ----------
    scene : Scene
        Scene containing photon data and wavelength sampling.

    Returns
    -------
    luminance : np.ndarray
        Luminance (cd/m^2) at each pixel.
    mean_luminance : float
        Mean luminance over the scene.
    """

    photons = np.asarray(scene.photons, dtype=float)
    luminance = luminance_from_photons(photons, scene.wave)
    mean_luminance = float(luminance.mean())
    return luminance, mean_luminance


__all__ = ["scene_calculate_luminance"]
