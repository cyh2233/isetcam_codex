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

    def __post_init__(self) -> None:
        if self.wave is None:
            init_default_spectrum(self)
