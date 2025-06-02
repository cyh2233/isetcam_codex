"""Retrieve parameters from :class:`Font` objects."""

from __future__ import annotations

from typing import Any

import numpy as np

from .font_class import Font
from ..ie_param_format import ie_param_format


def font_get(font: Font, param: str, *args) -> Any:
    """Return a parameter value from ``font``."""
    key = ie_param_format(param)
    if key == "type":
        return "font"
    if key == "name":
        return font.name
    if key == "character":
        return font.character
    if key == "size":
        return font.size
    if key == "family":
        return font.family
    if key == "style":
        return font.style
    if key == "dpi":
        return font.dpi
    if key == "bitmap":
        return font.bitmap
    if key == "ibitmap":
        return 1 - font.bitmap
    if key == "paddedbitmap":
        padsize = args[0] if len(args) > 0 else (7, 7)
        padval = args[1] if len(args) > 1 else 1
        bitmap = np.asarray(font.bitmap)
        out = np.full(
            (
                bitmap.shape[0] + 2 * padsize[0],
                bitmap.shape[1] + 2 * padsize[1],
                bitmap.shape[2],
            ),
            padval,
            dtype=bitmap.dtype,
        )
        out[
            padsize[0] : padsize[0] + bitmap.shape[0],
            padsize[1] : padsize[1] + bitmap.shape[1],
            :,
        ] = bitmap
        return out
    if key == "ipaddedbitmap":
        return 1 - font_get(font, "padded bitmap", *args)
    raise KeyError(f"Unknown font parameter '{param}'")


__all__ = ["font_get"]
