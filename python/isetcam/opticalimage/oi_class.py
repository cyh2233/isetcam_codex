"""Basic :class:`OpticalImage` dataclass."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class OpticalImage:
    """Minimal representation of an ISETCam optical image."""

    photons: np.ndarray
    wave: np.ndarray
    name: str | None = None
