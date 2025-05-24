"""Assign parameters on :class:`Display` objects."""

from __future__ import annotations

from typing import Any

import numpy as np

from .display_class import Display


def display_set(display: Display, param: str, val: Any) -> None:
    """Set a parameter value on ``display``.

    Supported parameters are ``spd``, ``wave``, ``gamma`` and ``name``.
    ``n_wave`` is a derived value and therefore cannot be set.
    """
    key = param.lower().replace(" ", "")
    if key == "spd":
        display.spd = np.asarray(val)
        return
    if key == "wave":
        display.wave = np.asarray(val)
        return
    if key == "gamma":
        display.gamma = None if val is None else np.asarray(val)
        return
    if key == "name":
        display.name = None if val is None else str(val)
        return
    raise KeyError(f"Unknown or read-only display parameter '{param}'")
