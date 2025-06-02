# mypy: ignore-errors
"""Resample a :class:`Scene` in the frequency domain."""

from __future__ import annotations

import numpy as np
from scipy.ndimage import zoom as nd_zoom

from .scene_class import Scene


def scene_frequency_resample(
    scene: Scene, n_rows: int, n_cols: int, method: str = "linear"
) -> Scene:
    """Resample ``scene`` so the frequency grid has ``n_rows`` by ``n_cols`` samples.

    The spatial field of view is preserved by adjusting the pixel spacing.
    """
    height, width = scene.photons.shape[:2]
    old_spacing = getattr(scene, "sample_spacing", 1.0)

    width_m = width * old_spacing
    height_m = height * old_spacing

    new_spacing_x = width_m / int(n_cols)
    new_spacing_y = height_m / int(n_rows)
    new_spacing = (new_spacing_x + new_spacing_y) / 2.0

    zoom_factors = (n_rows / height, n_cols / width, 1)

    orders = {"nearest": 0, "linear": 1, "cubic": 3}
    if method not in orders:
        raise ValueError("Unknown interpolation method")
    order = orders[method]

    resampled = nd_zoom(scene.photons, zoom_factors, order=order)
    out = Scene(photons=resampled, wave=scene.wave, name=scene.name)
    out.sample_spacing = new_spacing
    return out
