# mypy: ignore-errors
"""Scale scene illuminant so average reflectance is unity."""

from __future__ import annotations

import numpy as np

from .scene_class import Scene


def _expand_illuminant(illum: np.ndarray, shape: tuple[int, int, int]) -> np.ndarray:
    """Return ``illum`` expanded to ``shape``."""
    if illum.ndim == 1:
        if illum.size != shape[2]:
            raise ValueError("Illuminant vector length must match scene wave")
        return np.tile(illum.reshape(1, 1, -1), (shape[0], shape[1], 1))
    if illum.ndim == 3:
        if illum.shape != shape:
            raise ValueError("Illuminant cube must match scene photon shape")
        return illum
    raise ValueError("Illuminant must be 1-D or 3-D")


def scene_illuminant_scale(scene: Scene) -> Scene:
    """Adjust illuminant intensity to yield mean reflectance of one.

    Parameters
    ----------
    scene : Scene
        Input scene containing an ``illuminant`` attribute.

    Returns
    -------
    Scene
        New scene with scaled illuminant. Photon data are not modified.
    """

    illum = getattr(scene, "illuminant", None)
    if illum is None:
        raise AttributeError("scene has no illuminant attribute")

    photons = np.asarray(scene.photons, dtype=float)
    ill = np.asarray(illum, dtype=float)
    ill_cube = _expand_illuminant(ill, photons.shape)

    with np.errstate(divide="ignore", invalid="ignore"):
        refl = np.divide(photons, ill_cube, out=np.zeros_like(photons), where=ill_cube!=0)
    avg_refl = float(refl.mean())

    scale = avg_refl if avg_refl > 0 else 1.0
    new_illum = ill * scale

    out = Scene(photons=photons, wave=scene.wave, name=scene.name)
    if ill.ndim == 1:
        out.illuminant = new_illum
    else:
        out.illuminant = new_illum
    return out
