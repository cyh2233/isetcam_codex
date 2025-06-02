# mypy: ignore-errors
"""Retrieve spectral radiance at a pixel of a :class:`Scene`."""

from __future__ import annotations

import numpy as np

from .scene_class import Scene
from .scene_vector_utils import scene_photons_from_vector
from ..quanta2energy import quanta_to_energy


def scene_radiance_from_vector(scene: Scene, row: int, col: int) -> np.ndarray:
    """Return radiance at ``(row, col)`` as a 1-D vector.

    Parameters
    ----------
    scene : Scene
        Input scene containing photon data.
    row, col : int
        Pixel coordinates.

    Returns
    -------
    np.ndarray
        Radiance values in watts/sr/nm/m^2 for the given pixel.
    """
    photons_vec = scene_photons_from_vector(scene, row, col)
    energy = quanta_to_energy(scene.wave, photons_vec)
    return energy.reshape(-1)


__all__ = ["scene_radiance_from_vector"]
