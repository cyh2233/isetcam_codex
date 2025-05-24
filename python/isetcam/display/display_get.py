"""Retrieve parameters from :class:`Display` objects."""

from __future__ import annotations

from typing import Any

import numpy as np

from .display_class import Display
from ..ie_param_format import ie_param_format


def display_get(display: Display, param: str) -> Any:
    """Return a parameter value from ``display``.

    Supported parameters are ``spd``, ``wave``, ``n_wave``/``nwave``, ``gamma``
    and ``name``.
    """
    key = ie_param_format(param)
    if key == "spd":
        return display.spd
    if key == "wave":
        return display.wave
    if key == "gamma":
        return display.gamma
    if key in {"nwave", "n_wave"}:
        return len(display.wave)
    if key == "name":
        return getattr(display, "name", None)
    raise KeyError(f"Unknown display parameter '{param}'")
