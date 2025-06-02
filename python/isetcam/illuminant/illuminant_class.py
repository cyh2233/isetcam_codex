# mypy: ignore-errors
"""Basic :class:`Illuminant` dataclass."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class Illuminant:
    """Spectral power distribution of an illuminant."""

    spd: np.ndarray
    wave: np.ndarray
    name: str | None = None
