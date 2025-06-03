# mypy: ignore-errors
"""Assign parameters on :class:`OpticalImage` objects."""

from __future__ import annotations

from typing import Any

import numpy as np

from .oi_class import OpticalImage
from ..ie_param_format import ie_param_format


def oi_set(oi: OpticalImage, param: str, val: Any, units: str | None = None) -> None:
    """Set a parameter value on ``oi``.

    Supported parameters include ``photons``, ``wave``, ``name`` and basic optics
    properties.
    """
    key = ie_param_format(param)
    if key == "photons":
        oi.photons = np.asarray(val)
        return
    if key == "wave":
        oi.wave = np.asarray(val)
        return
    if key == "name":
        oi.name = None if val is None else str(val)
        return
    if key in {"opticsfnumber", "opticsf_number"}:
        oi.optics_f_number = float(val)
        return
    if key in {"opticsfocallength", "opticsf_length"}:
        length = float(val)
        if units == "mm":
            length /= 1e3
        oi.optics_f_length = length
        return
    if key == "opticsmodel":
        oi.optics_model = None if val is None else str(val)
        return
    raise KeyError(f"Unknown or read-only optical image parameter '{param}'")
