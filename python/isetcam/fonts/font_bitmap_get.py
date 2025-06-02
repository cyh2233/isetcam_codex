# mypy: ignore-errors
"""Return a bitmap for a :class:`Font`."""

from __future__ import annotations

from pathlib import Path

import numpy as np
from scipy.io import loadmat
from PIL import Image, ImageDraw, ImageFont

from ..data_path import data_path


_DEF_PAD = 3


def _bitmap_from_file(font: "Font") -> np.ndarray:
    path = data_path(Path("fonts") / f"{font.name}.mat")
    if not path.exists():
        raise FileNotFoundError
    mat = loadmat(path)
    bm_src = mat["bmSrc"][0, 0]
    b = 1 - bm_src["dataIndex"]
    padsize = 3 * int(np.ceil(b.shape[1] / 3)) - b.shape[1]
    if padsize > 0:
        b = np.pad(b, ((0, 0), (padsize, 0)), constant_values=1)
    width = int(np.ceil(b.shape[1] / 3))
    bitmap = np.ones((b.shape[0], width, 3), dtype=float)
    for ii in range(3):
        bitmap[:, :, ii] = b[:, ii::3]
    return bitmap


def _bitmap_from_pillow(font: "Font") -> np.ndarray:
    size = int(font.size * 2)
    try:
        pil_font = ImageFont.truetype(font.family, font.size, layout_engine=ImageFont.LAYOUT_BASIC)
    except Exception:
        pil_font = ImageFont.load_default()
    img = Image.new("L", (size, size), color=255)
    draw = ImageDraw.Draw(img)
    bbox = draw.textbbox((0, 0), font.character, font=pil_font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    draw.text(((size - w) / 2, (size - h) / 2), font.character, fill=0, font=pil_font)
    arr = np.array(img)
    mask = arr < 255
    if mask.any():
        rows = np.where(mask.any(axis=1))[0]
        cols = np.where(mask.any(axis=0))[0]
        arr = arr[rows[0] : rows[-1] + 1, cols[0] : cols[-1] + 1]
    bitmap = (arr <= 127).astype(float)
    return np.repeat(bitmap[:, :, None], 3, axis=2)


def font_bitmap_get(font: "Font") -> np.ndarray:
    """Return the bitmap image for ``font``."""
    try:
        return _bitmap_from_file(font)
    except Exception:
        return _bitmap_from_pillow(font)


__all__ = ["font_bitmap_get"]
