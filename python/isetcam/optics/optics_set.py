# mypy: ignore-errors
"""Assign parameters on :class:`Optics` objects."""

from __future__ import annotations

from typing import Any

import numpy as np

from .optics_class import Optics
from ..ie_param_format import ie_param_format


def optics_set(optics: Optics, param: str, val: Any) -> None:
    """Set a parameter value on ``optics``."""
    key = ie_param_format(param)
    if key in {"fnumber", "f_number"}:
        optics.f_number = float(val)
        return
    if key in {"offaxismethod", "off_axis_method"}:
        optics.off_axis_method = None if val is None else str(val)
        return
    if key in {"flength", "focallength", "f_length"}:
        optics.f_length = float(val)
        return
    if key == "wave":
        optics.wave = np.asarray(val, dtype=float).reshape(-1)
        if optics.transmittance is not None and optics.transmittance.size != optics.wave.size:  # noqa: E501
            optics.transmittance = np.ones_like(optics.wave, dtype=float)
        return
    if key == "transmittance":
        optics.transmittance = np.asarray(val, dtype=float)
        return
    if key == "name":
        optics.name = None if val is None else str(val)
        return
    raise KeyError(f"Unknown or read-only optics parameter '{param}'")
