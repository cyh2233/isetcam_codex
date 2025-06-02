# mypy: ignore-errors
"""Retrieve parameters from :class:`Optics` objects."""

from __future__ import annotations

from typing import Any

import numpy as np

from .optics_class import Optics
from ..ie_param_format import ie_param_format


def optics_get(optics: Optics, param: str) -> Any:
    """Return a parameter value from ``optics``."""
    key = ie_param_format(param)
    if key in {"fnumber", "f_number"}:
        return optics.f_number
    if key in {"flength", "focallength", "f_length"}:
        return optics.f_length
    if key == "wave":
        return optics.wave
    if key in {"nwave", "n_wave"}:
        return len(optics.wave)
    if key == "transmittance":
        return optics.transmittance
    if key == "name":
        return getattr(optics, "name", None)
    raise KeyError(f"Unknown optics parameter '{param}'")
