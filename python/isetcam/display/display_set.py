# mypy: ignore-errors
"""Assign parameters on :class:`Display` objects."""

from __future__ import annotations

from typing import Any

import numpy as np

from .display_class import Display
from ..ie_param_format import ie_param_format


def display_set(display: Display, param: str, val: Any) -> None:
    """Set a parameter value on ``display``.

    Supported parameters are ``spd``, ``wave``, ``gamma``, ``max_luminance`` and
    ``white_point`` as well as ``name``. ``n_wave`` is a derived value and
    therefore cannot be set.
    """
    key = ie_param_format(param)
    if key == "spd":
        display.spd = np.asarray(val)
        return
    if key == "wave":
        display.wave = np.asarray(val)
        return
    if key == "gamma":
        display.gamma = None if val is None else np.asarray(val)
        return
    if key in {"maxluminance", "max_luminance"}:
        display.max_luminance = None if val is None else float(val)
        return
    if key in {"whitepoint", "white_point"}:
        display.white_point = None if val is None else np.asarray(val, dtype=float)
        return
    if key == "name":
        display.name = None if val is None else str(val)
        return
    raise KeyError(f"Unknown or read-only display parameter '{param}'")
