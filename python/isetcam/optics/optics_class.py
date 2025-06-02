# mypy: ignore-errors
"""Basic :class:`Optics` dataclass."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ..init_default_spectrum import init_default_spectrum


@dataclass
class Optics:
    """Minimal representation of ISETCam optics."""

    f_number: float
    f_length: float
    wave: np.ndarray | None = None
    transmittance: np.ndarray | None = None
    name: str | None = None

    def __post_init__(self) -> None:
        if self.wave is None:
            init_default_spectrum(self)
        else:
            self.wave = np.asarray(self.wave, dtype=float).reshape(-1)
        if self.transmittance is None:
            self.transmittance = np.ones_like(self.wave, dtype=float)
        else:
            self.transmittance = np.asarray(self.transmittance, dtype=float)
