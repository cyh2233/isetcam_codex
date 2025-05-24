"""Assign parameters on :class:`Sensor` objects."""

from __future__ import annotations

from typing import Any

import numpy as np

from .sensor_class import Sensor
from ..ie_param_format import ie_param_format


def sensor_set(sensor: Sensor, param: str, val: Any) -> None:
    """Set a parameter value on ``sensor``.

    Supported parameters are ``volts``, ``wave``, ``exposure_time``/``exposure time``
    and ``name``. ``n_wave`` is derived from ``wave`` and therefore cannot be set.
    """
    key = ie_param_format(param)
    if key == "volts":
        sensor.volts = np.asarray(val)
        return
    if key == "wave":
        sensor.wave = np.asarray(val)
        return
    if key in {"exposure_time", "exposuretime"}:
        sensor.exposure_time = float(val)
        return
    if key == "name":
        sensor.name = None if val is None else str(val)
        return
    raise KeyError(f"Unknown or read-only sensor parameter '{param}'")
