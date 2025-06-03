# mypy: ignore-errors
"""Basic :class:`OpticalImage` dataclass."""

from __future__ import annotations

from dataclasses import dataclass

from ..init_default_spectrum import init_default_spectrum

import numpy as np


@dataclass
class OpticalImage:
    """Minimal representation of an ISETCam optical image."""

    photons: np.ndarray
    wave: np.ndarray | None = None
    name: str | None = None
    optics_f_number: float = 0.0
    optics_f_length: float = 0.0
    optics_model: str = ""

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
