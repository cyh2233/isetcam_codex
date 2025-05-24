"""Retrieve parameters from :class:`Display` objects."""

from __future__ import annotations

from typing import Any

import numpy as np

from .display_class import Display


def display_get(display: Display, param: str) -> Any:
    """Return a parameter value from ``display``.

    Supported parameters are ``spd``, ``wave``, ``n_wave``/``nwave`` and
    ``name``.
    """
    key = param.lower().replace(" ", "")
    if key == "spd":
        return display.spd
    if key == "wave":
        return display.wave
    if key in {"nwave", "n_wave"}:
        return len(display.wave)
    if key == "name":
        return getattr(display, "name", None)
    raise KeyError(f"Unknown display parameter '{param}'")
