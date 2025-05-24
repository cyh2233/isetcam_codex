"""Retrieve parameters from :class:`Camera` objects."""

from __future__ import annotations

from typing import Any

from .camera_class import Camera


def camera_get(camera: Camera, param: str) -> Any:
    """Return a parameter value from ``camera``.

    Supported parameters are ``sensor``, ``optical_image``/``oi``, ``name``
    and ``n_wave``/``nwave`` (derived from the sensor's wavelength sampling).
    """
    key = param.lower().replace(" ", "").replace("_", "")
    if key == "sensor":
        return camera.sensor
    if key in {"opticalimage", "oi"}:
        return camera.optical_image
    if key in {"nwave", "n_wave"}:
        return len(camera.sensor.wave)
    if key == "name":
        return getattr(camera, "name", None)
    raise KeyError(f"Unknown camera parameter '{param}'")
