# mypy: ignore-errors
"""Apply a spatial pattern to the scene illuminant and photons."""

from __future__ import annotations

import numpy as np
from scipy.ndimage import zoom as nd_zoom

from .scene_class import Scene


def scene_illuminant_pattern(scene: Scene, pattern: np.ndarray) -> Scene:
    """Multiply ``scene`` photons and illuminant by ``pattern``.

    Parameters
    ----------
    scene : Scene
        Input scene containing an ``illuminant`` attribute.
    pattern : array-like
        2-D spatial pattern used to modulate the photons and illuminant.

    Returns
    -------
    Scene
        New scene with scaled photons and illuminant.
    """

    pat = np.asarray(pattern, dtype=float)
    if pat.ndim != 2:
        raise ValueError("pattern must be 2-D")

    photons = np.asarray(scene.photons, dtype=float)
    rows, cols = photons.shape[:2]
    if pat.shape != (rows, cols):
        zoom_factors = (rows / pat.shape[0], cols / pat.shape[1])
        pat = nd_zoom(pat, zoom_factors, order=1)

    scaled_photons = photons * pat[:, :, np.newaxis]
    out = Scene(photons=scaled_photons, wave=scene.wave, name=scene.name)

    illum = getattr(scene, "illuminant", None)
    if illum is not None:
        ill = np.asarray(illum, dtype=float)
        if ill.ndim == 1:
            if ill.size != photons.shape[2]:
                raise ValueError("Illuminant vector length must match scene wave")
            ill = np.tile(ill.reshape(1, 1, -1), (rows, cols, 1))
        elif ill.ndim == 3:
            if ill.shape != photons.shape:
                raise ValueError("Illuminant cube must match scene photon shape")
        else:
            raise ValueError("Illuminant must be 1-D or 3-D")
        ill = ill * pat[:, :, np.newaxis]
        if np.allclose(ill, ill[0, 0, :]):
            out.illuminant = ill[0, 0, :]
        else:
            out.illuminant = ill

    return out
