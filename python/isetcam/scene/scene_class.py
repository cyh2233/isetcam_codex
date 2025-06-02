# mypy: ignore-errors
"""Basic :class:`Scene` dataclass."""

from __future__ import annotations

from dataclasses import dataclass

from ..init_default_spectrum import init_default_spectrum

import numpy as np


@dataclass
class Scene:
    """Minimal representation of an ISETCam scene."""

    photons: np.ndarray
    wave: np.ndarray | None = None
    name: str | None = None
    distance: float | None = None
    fov: float | None = None

    def __post_init__(self) -> None:
        if self.wave is None:
            init_default_spectrum(self)

    def __repr__(self) -> str:
        """Return a concise representation for debugging."""
        shape = tuple(self.photons.shape)
        if self.wave is None or self.wave.size == 0:
            wave_range = "None"
        else:
            wave_range = f"({float(self.wave[0])}, {float(self.wave[-1])})"
        return (
            f"{self.__class__.__name__}(name={self.name!r}, "
            f"shape={shape}, wave_range={wave_range})"
        )
