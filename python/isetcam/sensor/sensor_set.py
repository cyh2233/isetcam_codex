# mypy: ignore-errors
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
    Noise related parameters (``conversion_gain``, ``read_noise_electrons``,
    ``gain_sd``, ``offset_sd`` and ``voltage_swing``) are stored as attributes on
    ``sensor`` when supplied.
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
    if key in {"conversiongain", "conversion_gain"}:
        sensor.conversion_gain = float(val)
        return
    if key in {"readnoiseelectrons", "read_noise_electrons"}:
        sensor.read_noise_electrons = float(val)
        return
    if key in {"gainsd", "gain_sd"}:
        sensor.gain_sd = float(val)
        return
    if key in {"offsetsd", "offset_sd"}:
        sensor.offset_sd = float(val)
        return
    if key in {"voltageswing", "voltage_swing"}:
        sensor.voltage_swing = float(val)
        return
    raise KeyError(f"Unknown or read-only sensor parameter '{param}'")
