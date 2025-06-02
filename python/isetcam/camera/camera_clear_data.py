# mypy: ignore-errors
"""Utility to remove optional attributes from a Camera and its components."""

from __future__ import annotations

from .camera_class import Camera
from ..opticalimage import oi_clear_data
from ..sensor import sensor_clear_data
from ..ip import ip_clear_data


def camera_clear_data(camera: Camera) -> Camera:
    """Remove cached or optional attributes from ``camera``.

    This invokes :func:`oi_clear_data`, :func:`sensor_clear_data` and
    :func:`ip_clear_data` on the optical image, sensor and image
    processor objects of ``camera`` respectively.
    """
    camera.optical_image = oi_clear_data(camera.optical_image)
    camera.sensor = sensor_clear_data(camera.sensor)
    if hasattr(camera, "ip"):
        camera.ip = ip_clear_data(camera.ip)
    return camera


__all__ = ["camera_clear_data"]
