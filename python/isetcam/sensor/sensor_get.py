"""Retrieve parameters from :class:`Sensor` objects."""

from __future__ import annotations

from typing import Any

import numpy as np

from .sensor_class import Sensor
from ..ie_param_format import ie_param_format


def sensor_get(sensor: Sensor, param: str) -> Any:
    """Return a parameter value from ``sensor``.

    Supported parameters are ``volts``, ``wave``, ``n_wave``/``nwave``,
    ``exposure_time``/``exposure time`` and ``name``.
    """
    key = ie_param_format(param)
    if key == "volts":
        return sensor.volts
    if key == "wave":
        return sensor.wave
    if key in {"nwave", "n_wave"}:
        return len(sensor.wave)
    if key in {"exposure_time", "exposuretime"}:
        return sensor.exposure_time
    if key == "name":
        return getattr(sensor, "name", None)
    raise KeyError(f"Unknown sensor parameter '{param}'")
