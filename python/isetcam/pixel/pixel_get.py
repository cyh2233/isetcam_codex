# mypy: ignore-errors
"""Retrieve parameters from :class:`Pixel` objects."""

from __future__ import annotations

from typing import Any

from .pixel_class import Pixel
from ..ie_param_format import ie_param_format


def pixel_get(pixel: Pixel, param: str) -> Any:
    """Return a parameter value from ``pixel``."""
    key = ie_param_format(param)
    if key == "width":
        return pixel.width
    if key == "height":
        return pixel.height
    if key in {"wellcapacity", "well_capacity"}:
        return pixel.well_capacity
    if key in {"fillfactor", "fill_factor"}:
        return pixel.fill_factor
    raise KeyError(f"Unknown pixel parameter '{param}'")
