"""Assign parameters on :class:`Pixel` objects."""

from __future__ import annotations

from typing import Any

from .pixel_class import Pixel
from ..ie_param_format import ie_param_format


def pixel_set(pixel: Pixel, param: str, val: Any) -> None:
    """Set a parameter value on ``pixel``."""
    key = ie_param_format(param)
    if key == "width":
        pixel.width = float(val)
        return
    if key == "height":
        pixel.height = float(val)
        return
    if key in {"wellcapacity", "well_capacity"}:
        pixel.well_capacity = float(val)
        return
    if key in {"fillfactor", "fill_factor"}:
        pixel.fill_factor = float(val)
        return
    raise KeyError(f"Unknown pixel parameter '{param}'")
