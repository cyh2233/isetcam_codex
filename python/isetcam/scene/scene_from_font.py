"""Create a simple :class:`Scene` from text rendered with a :class:`Font`."""

from __future__ import annotations

from typing import Optional

import numpy as np

from .scene_class import Scene
from ..fonts import Font, font_create, font_bitmap_get


_DEF_SPACING = 1


def scene_from_font(text: str, font: Optional[Font] = None, spacing: int = _DEF_SPACING) -> Scene:
    """Return a :class:`Scene` built from ``text`` using ``font``.

    Parameters
    ----------
    text:
        Text string to render.
    font:
        Base :class:`Font` describing size and family. The ``character`` field is
        ignored and each character from ``text`` is rendered individually.
    spacing:
        Number of blank columns inserted between characters.
    """
    if spacing < 0:
        raise ValueError("spacing must be non-negative")
    if font is None:
        font = font_create()

    char_fonts = []
    for ch in text:
        f = Font(
            character=ch,
            family=font.family,
            size=font.size,
            dpi=font.dpi,
            style=font.style,
        )
        f.bitmap = font_bitmap_get(f)
        char_fonts.append(f)

    height = max(f.bitmap.shape[0] for f in char_fonts)
    width = sum(f.bitmap.shape[1] for f in char_fonts) + spacing * (len(char_fonts) - 1)
    img = np.ones((height, width, 3), dtype=float)

    col = 0
    for f in char_fonts:
        bm = f.bitmap
        top = (height - bm.shape[0]) // 2
        img[top : top + bm.shape[0], col : col + bm.shape[1], :] = bm
        col += bm.shape[1] + spacing

    wave = np.arange(3)
    scene = Scene(photons=img, wave=wave, name=text)
    return scene


__all__ = ["scene_from_font"]
