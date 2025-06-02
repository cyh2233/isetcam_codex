# mypy: ignore-errors
"""Scale the spectral power distribution of a scene."""

from __future__ import annotations

import numpy as np

from .scene_class import Scene


def scene_spd_scale(scene: Scene, scale: float) -> Scene:
    """Multiply the photon data of ``scene`` by ``scale``.

    Parameters
    ----------
    scene : Scene
        Input scene whose photons will be scaled.
    scale : float
        Multiplicative factor applied to the photons.

    Returns
    -------
    Scene
        New scene with scaled photons. The name is updated to reflect the
        scaling factor.
    """

    photons = np.asarray(scene.photons, dtype=float)
    scaled_photons = photons * float(scale)

    if scene.name:
        name = f"{scene.name} x{scale}" if scale != 1 else scene.name
    else:
        name = None

    return Scene(photons=scaled_photons, wave=scene.wave, name=name)
