"""Basic :class:`VCImage` dataclass."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class VCImage:
    """Minimal view controller image container."""

    rgb: np.ndarray
    wave: np.ndarray
    name: str | None = None
