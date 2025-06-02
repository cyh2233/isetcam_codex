# mypy: ignore-errors
"""Assign parameters on :class:`Font` objects."""

from __future__ import annotations

from typing import Any

from .font_class import Font
from ..ie_param_format import ie_param_format
from .font_bitmap_get import font_bitmap_get


def font_set(font: Font, param: str, val: Any) -> Font:
    """Set a parameter value on ``font``."""
    key = ie_param_format(param)
    if key == "type":
        return font
    if key == "name":
        font.name = str(val)
    elif key == "character":
        font.character = str(val)
    elif key == "size":
        font.size = int(val)
    elif key == "family":
        font.family = str(val)
    elif key == "style":
        font.style = str(val)
    elif key == "dpi":
        font.dpi = int(val)
    elif key == "bitmap":
        font.bitmap = val
        return font
    else:
        raise KeyError(f"Unknown font parameter '{param}'")

    font.name = f"{font.character}-{font.family}-{font.size}-{font.dpi}".lower()
    font.bitmap = font_bitmap_get(font)
    return font


__all__ = ["font_set"]
