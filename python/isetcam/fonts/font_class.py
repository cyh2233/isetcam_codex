from __future__ import annotations

from dataclasses import dataclass
import numpy as np


@dataclass
class Font:
    """Simple font description used for rendering text."""

    character: str = "g"
    family: str = "DejaVuSans"
    size: int = 14
    dpi: int = 96
    style: str = "NORMAL"
    bitmap: np.ndarray | None = None
    name: str | None = None

    def __post_init__(self) -> None:
        if self.name is None:
            self.name = f"{self.character}-{self.family}-{self.size}-{self.dpi}".lower()
        if self.bitmap is None:
            from .font_bitmap_get import font_bitmap_get

            self.bitmap = font_bitmap_get(self)
