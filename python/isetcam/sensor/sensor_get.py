# mypy: ignore-errors
"""Retrieve parameters from :class:`Sensor` objects."""

from __future__ import annotations

from typing import Any

import numpy as np

from .sensor_class import Sensor
from ..ie_param_format import ie_param_format


def sensor_get(sensor: Sensor, param: str) -> Any:
    """Return a parameter value from ``sensor``.

    Supported parameters are ``volts``, ``wave``, ``n_wave``/``nwave``,
    ``exposure_time``/``exposure time`` and ``name``.  Additional optional
    noise related parameters are ``conversion_gain``, ``read_noise_electrons``,
    ``gain_sd`` (in percent), ``offset_sd`` and ``voltage_swing``.  These are
    returned as attributes on ``sensor`` and default to sensible values when
    absent.
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
    if key in {"conversiongain", "conversion_gain"}:
        return getattr(sensor, "conversion_gain", 1.0)
    if key in {"readnoiseelectrons", "read_noise_electrons"}:
        return getattr(sensor, "read_noise_electrons", 0.0)
    if key in {"gainsd", "gain_sd"}:
        return getattr(sensor, "gain_sd", 0.0)
    if key in {"offsetsd", "offset_sd"}:
        return getattr(sensor, "offset_sd", 0.0)
    if key in {"voltageswing", "voltage_swing"}:
        return getattr(sensor, "voltage_swing", 1.0)
    if key in {"ncolors", "n_colors"}:
        if hasattr(sensor, "n_colors") and sensor.n_colors is not None:
            return sensor.n_colors
        return sensor.volts.shape[2] if sensor.volts.ndim == 3 else 1
    if key in {"filtercolorletters", "filter_color_letters"}:
        return getattr(sensor, "filter_color_letters", None)
    raise KeyError(f"Unknown sensor parameter '{param}'")
