# mypy: ignore-errors
"""Retrieve parameters from :class:`Illuminant` objects."""

from __future__ import annotations

from typing import Any

import numpy as np

from .illuminant_class import Illuminant
from ..ie_param_format import ie_param_format


def illuminant_get(illuminant: Illuminant, param: str) -> Any:
    """Return a parameter value from ``illuminant``.

    Supported parameters are ``spd``, ``wave``, ``n_wave``/``nwave`` and ``name``.
    """
    key = ie_param_format(param)
    if key == "spd":
        return illuminant.spd
    if key == "wave":
        return illuminant.wave
    if key in {"nwave", "n_wave"}:
        return len(illuminant.wave)
    if key == "name":
        return getattr(illuminant, "name", None)
    raise KeyError(f"Unknown illuminant parameter '{param}'")
