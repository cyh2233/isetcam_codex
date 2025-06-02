# mypy: ignore-errors
"""Adjust scene luminance by scaling photon data."""

from __future__ import annotations

import numpy as np

from .scene_class import Scene
from ..luminance_from_photons import luminance_from_photons
from .scene_utils import get_photons, set_photons


VALID_METHODS = {"mean", "peak", "max"}


def scene_adjust_luminance(scene: Scene, method: str, target_l: float) -> Scene:
    """Scale ``scene`` so a luminance statistic equals ``target_l``.

    Parameters
    ----------
    scene : Scene
        Input scene to scale.
    method : {"mean", "peak"}
        Luminance statistic used for scaling.
    target_l : float
        Desired luminance level in cd/m^2.

    Returns
    -------
    Scene
        New scene with scaled photon data.
    """

    flag = method.lower().replace(" ", "")
    if flag not in VALID_METHODS:
        raise ValueError(f"Unknown method '{method}'")

    photons = np.asarray(get_photons(scene), dtype=float)
    lum = luminance_from_photons(photons, scene.wave)

    if flag == "mean":
        current = float(lum.mean())
    else:  # peak or max
        current = float(lum.max())

    if current > 0:
        photons = photons * (target_l / current)

    out = Scene(photons=photons, wave=scene.wave, name=scene.name)
    return out

