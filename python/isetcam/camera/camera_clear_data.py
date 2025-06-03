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
    if getattr(camera.optical_image, "name", None) is None:
        camera.optical_image.name = ""
    if getattr(camera.sensor, "name", None) is None:
        camera.sensor.name = ""
    if getattr(camera.optical_image, "optics_model", None) is None:
        camera.optical_image.optics_model = ""
    if getattr(camera, "name", None) is None:
        camera.name = ""
    if hasattr(camera, "ip"):
        camera.ip = ip_clear_data(camera.ip)
    return camera


__all__ = ["camera_clear_data"]
