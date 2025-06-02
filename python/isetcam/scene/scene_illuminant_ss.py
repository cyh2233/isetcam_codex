# mypy: ignore-errors
"""Convert a scene illuminant to spatial-spectral format."""

from __future__ import annotations

import numpy as np

from .scene_class import Scene
from .scene_illuminant_pattern import scene_illuminant_pattern


def scene_illuminant_ss(scene: Scene, pattern: np.ndarray | None = None) -> Scene:
    """Ensure the scene illuminant is spatial-spectral.

    Parameters
    ----------
    scene : Scene
        Input scene with an ``illuminant`` attribute.
    pattern : array-like, optional
        Spatial pattern applied after conversion.

    Returns
    -------
    Scene
        Scene with spatial-spectral illuminant, optionally scaled by ``pattern``.
    """

    photons = np.asarray(scene.photons, dtype=float)
    rows, cols, n_wave = photons.shape

    illum = getattr(scene, "illuminant", None)
    if illum is None:
        raise AttributeError("scene has no illuminant attribute")
    ill = np.asarray(illum, dtype=float)

    if ill.ndim == 1:
        if ill.size != n_wave:
            raise ValueError("Illuminant vector length must match scene wave")
        ill_cube = np.tile(ill.reshape(1, 1, -1), (rows, cols, 1))
    elif ill.ndim == 3:
        if ill.shape != photons.shape:
            raise ValueError("Illuminant cube must match scene photon shape")
        ill_cube = ill
    else:
        raise ValueError("Illuminant must be 1-D or 3-D")

    out = Scene(photons=photons, wave=scene.wave, name=scene.name)
    out.illuminant = ill_cube

    if pattern is not None:
        out = scene_illuminant_pattern(out, pattern)

    return out
