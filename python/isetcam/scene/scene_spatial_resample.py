# mypy: ignore-errors
"""Resample a :class:`Scene` while preserving field of view."""

from __future__ import annotations

import numpy as np
from scipy.ndimage import zoom as nd_zoom

from .scene_class import Scene


def _unit_to_meters(units: str) -> float:
    units = units.lower()
    if units in {"m", "meter", "meters"}:
        return 1.0
    if units in {"mm", "millimeter", "millimeters"}:
        return 1e-3
    if units in {"um", "micron", "microns", "micrometer", "micrometers"}:
        return 1e-6
    raise ValueError(f"Unknown spatial unit '{units}'")


def scene_spatial_resample(
    scene: Scene, dx: float, units: str = "m", method: str = "linear"
) -> Scene:
    """Resample ``scene`` to new pixel spacing ``dx``.

    Parameters
    ----------
    scene : Scene
        Input scene.
    dx : float
        Desired pixel spacing.
    units : str, optional
        Units for ``dx``. Defaults to meters.
    method : {{"linear", "nearest", "cubic"}}, optional
        Interpolation method. Defaults to "linear".

    Returns
    -------
    Scene
        Scene resampled to the new pixel spacing with the same field of view.
    """
    old_spacing = getattr(scene, "sample_spacing", 1.0)
    new_spacing = float(dx) * _unit_to_meters(units)

    height, width = scene.photons.shape[:2]
    width_m = width * old_spacing
    height_m = height * old_spacing

    new_width = max(int(round(width_m / new_spacing)), 1)
    new_height = max(int(round(height_m / new_spacing)), 1)

    zoom_factors = (new_height / height, new_width / width, 1)

    orders = {"nearest": 0, "linear": 1, "cubic": 3}
    if method not in orders:
        raise ValueError("Unknown interpolation method")
    order = orders[method]

    resampled = nd_zoom(scene.photons, zoom_factors, order=order)
    out = Scene(photons=resampled, wave=scene.wave, name=scene.name)
    out.sample_spacing = new_spacing
    return out

