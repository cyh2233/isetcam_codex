"""Basic :class:`Scene` dataclass."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class Scene:
    """Minimal representation of an ISETCam scene."""

    photons: np.ndarray
    wave: np.ndarray
    name: str | None = None
