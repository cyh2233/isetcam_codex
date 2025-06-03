# mypy: ignore-errors
"""Assign parameters on :class:`Camera` objects.

Keys beginning with ``"optics"`` or ``"ip"`` are forwarded to
``optics_set`` and ``ip_set`` respectively when the corresponding
attribute is present on ``camera``.
"""

from __future__ import annotations

from typing import Any

from .camera_class import Camera
from ..ie_param_format import ie_param_format
from ..optics import optics_set
from ..ip import ip_set


def camera_set(camera: Camera, param: str, val: Any) -> None:
    """Set a parameter value on ``camera``.

    Supported parameters are ``sensor``, ``optical_image``/``oi`` and
    ``name``. ``n_wave`` is derived from the sensor and cannot be set.
    """
    # check for sub-object dispatch before normalizing completely
    raw = str(param).strip()
    low = raw.lower()
    if low.startswith("optics"):
        sub = raw[6:].strip()
        if not hasattr(camera, "optics"):
            raise KeyError("Camera has no 'optics' attribute")
        if not sub:
            camera.optics = val
        else:
            optics_set(camera.optics, sub, val)
        return
    if low.startswith("ip"):
        sub = raw[2:].strip()
        if not hasattr(camera, "ip"):
            raise KeyError("Camera has no 'ip' attribute")
        if not sub:
            camera.ip = val
        else:
            ip_set(camera.ip, sub, val)
        return

    key = ie_param_format(raw).replace("_", "")
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


__all__ = ["camera_set"]
