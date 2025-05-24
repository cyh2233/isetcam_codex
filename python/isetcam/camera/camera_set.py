"""Assign parameters on :class:`Camera` objects."""

from __future__ import annotations

from typing import Any

from .camera_class import Camera
from ..ie_param_format import ie_param_format


def camera_set(camera: Camera, param: str, val: Any) -> None:
    """Set a parameter value on ``camera``.

    Supported parameters are ``sensor``, ``optical_image``/``oi`` and
    ``name``. ``n_wave`` is derived from the sensor and cannot be set.
    """
    key = ie_param_format(param).replace("_", "")
    if key == "sensor":
        camera.sensor = val
        return
    if key in {"opticalimage", "oi"}:
        camera.optical_image = val
        return
    if key == "name":
        camera.name = None if val is None else str(val)
        return
    if key in {"nwave", "n_wave"}:
        raise KeyError("'n_wave' is read-only and derived from the sensor")
    raise KeyError(f"Unknown camera parameter '{param}'")
