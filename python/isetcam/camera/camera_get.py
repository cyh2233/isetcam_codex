# mypy: ignore-errors
"""Retrieve parameters from :class:`Camera` objects.

Keys beginning with ``"optics"`` or ``"ip"`` are forwarded to
``optics_get`` and ``ip_get`` respectively when the corresponding
attribute is present on ``camera``.  For example ``"optics fnumber"``
returns ``optics_get(camera.optics, "fnumber")``.
"""

from __future__ import annotations

from typing import Any

from .camera_class import Camera
from ..ie_param_format import ie_param_format
from ..optics import optics_get
from ..ip import ip_get


def camera_get(camera: Camera, param: str) -> Any:
    """Return a parameter value from ``camera``.

    Supported parameters are ``sensor``, ``optical_image``/``oi``, ``name``
    and ``n_wave``/``nwave`` (derived from the sensor's wavelength sampling).
    """
    # check for sub-object dispatch before normalizing completely
    raw = str(param).strip()
    low = raw.lower()
    if low.startswith("optics"):
        sub = raw[6:].strip()
        if not hasattr(camera, "optics"):
            raise KeyError("Camera has no 'optics' attribute")
        if not sub:
            return camera.optics
        return optics_get(camera.optics, sub)
    if low.startswith("ip"):
        sub = raw[2:].strip()
        if not hasattr(camera, "ip"):
            raise KeyError("Camera has no 'ip' attribute")
        if not sub:
            return camera.ip
        return ip_get(camera.ip, sub)

    key = ie_param_format(raw).replace("_", "")
    if key == "sensor":
        return camera.sensor
    if key in {"opticalimage", "oi"}:
        return camera.optical_image
    if key in {"nwave", "n_wave"}:
        return len(camera.sensor.wave)
    if key == "name":
        return getattr(camera, "name", None)
    raise KeyError(f"Unknown camera parameter '{param}'")


__all__ = ["camera_get"]
