# mypy: ignore-errors
"""Replace scene reflectance while keeping the illuminant constant."""

from __future__ import annotations

import numpy as np

from .scene_class import Scene


def _broadcast_vector(vec: np.ndarray, shape: tuple[int, int, int]) -> np.ndarray:
    """Return ``vec`` expanded to ``shape``."""
    return np.tile(vec.reshape(1, 1, -1), (shape[0], shape[1], 1))


def scene_adjust_reflectance(scene: Scene, new_reflectance: np.ndarray) -> Scene:
    """Adjust the scene reflectance keeping the original illuminant.

    Parameters
    ----------
    scene : Scene
        Input scene to adjust.
    new_reflectance : array-like
        New reflectance values. Can be a 1-D vector of length ``scene.wave``
        or a 3-D array matching ``scene.photons``.

    Returns
    -------
    Scene
        New scene with photons recomputed from the preserved illuminant and
        ``new_reflectance``.
    """

    photons = np.asarray(scene.photons, dtype=float)
    wave_len = photons.shape[2]
    shape = photons.shape

    refl = np.asarray(new_reflectance, dtype=float)
    if refl.ndim == 1:
        if refl.size != wave_len:
            raise ValueError("Reflectance vector length must match scene wave")
        refl_cube = _broadcast_vector(refl, shape)
    elif refl.ndim == 3:
        if refl.shape != shape:
            raise ValueError("Reflectance cube must match scene photon shape")
        refl_cube = refl
    else:
        raise ValueError("new_reflectance must be 1-D or 3-D")

    illum = getattr(scene, "illuminant", None)
    if illum is not None:
        illum = np.asarray(illum, dtype=float)
        if illum.ndim == 1:
            if illum.size != wave_len:
                raise ValueError("Illuminant vector length must match scene wave")
            illum_cube = _broadcast_vector(illum, shape)
        elif illum.ndim == 3:
            if illum.shape != shape:
                raise ValueError("Illuminant cube must match scene photon shape")
            illum_cube = illum
        else:
            raise ValueError("Illuminant must be 1-D or 3-D")
    else:
        old_refl = getattr(scene, "reflectance", None)
        if old_refl is not None:
            old = np.asarray(old_refl, dtype=float)
            if old.ndim == 1:
                if old.size != wave_len:
                    raise ValueError("Reflectance vector length must match scene wave")
                old_cube = _broadcast_vector(old, shape)
            elif old.ndim == 3:
                if old.shape != shape:
                    raise ValueError("Reflectance cube must match scene photon shape")
                old_cube = old
            else:
                raise ValueError("Reflectance must be 1-D or 3-D")
            with np.errstate(divide="ignore", invalid="ignore"):
                illum_cube = np.divide(photons, old_cube, out=np.zeros_like(photons), where=old_cube!=0)  # noqa: E501
        else:
            illum_vec = photons.mean(axis=(0, 1))
            illum_cube = _broadcast_vector(illum_vec, shape)

    new_photons = refl_cube * illum_cube

    out = Scene(photons=new_photons, wave=scene.wave, name=scene.name)
    if illum is not None:
        out.illuminant = illum
    else:
        # store a vector when the illuminant is uniform across space
        if np.allclose(illum_cube, illum_cube[0, 0, :]):
            out.illuminant = illum_cube[0, 0, :]
        else:
            out.illuminant = illum_cube
    out.reflectance = new_reflectance
    return out
