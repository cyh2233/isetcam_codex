# mypy: ignore-errors
"""Match scene sampling to a target pixel size."""

from __future__ import annotations

import math

from .scene_class import Scene
from ..opticalimage.oi_class import OpticalImage


def scene_adjust_pixel_size(scene: Scene, oi: OpticalImage, pixel_size: float) -> tuple[Scene, float]:  # noqa: E501
    """Adjust scene distance so sample spacing equals ``pixel_size``.

    Parameters
    ----------
    scene : Scene
        Input scene whose distance and field of view will be updated.
    oi : OpticalImage
        Optical image used with ``scene``. Currently unused but kept for
        compatibility with the MATLAB function.
    pixel_size : float
        Desired pixel size in meters.

    Returns
    -------
    Scene
        Scene with updated ``distance`` and ``fov`` attributes.
    float
        The new scene distance in meters.
    """
    current_distance = getattr(scene, "distance", 1.0)
    sample_spacing = getattr(scene, "sample_spacing", 1.0)

    new_distance = current_distance * (pixel_size / sample_spacing)
    scene.distance = new_distance

    width_pixels = scene.photons.shape[1]
    sensor_width = pixel_size * width_pixels
    scene.fov = 2 * math.degrees(math.atan(sensor_width / (2 * new_distance)))

    return scene, new_distance

