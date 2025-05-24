"""Basic :class:`Display` dataclass."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class Display:
    """Minimal representation of an ISETCam display."""

    spd: np.ndarray
    wave: np.ndarray
    name: str | None = None
