"""Basic :class:`Sensor` dataclass."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class Sensor:
    """Minimal representation of an ISETCam sensor."""

    volts: np.ndarray
    wave: np.ndarray
    exposure_time: float
    name: str | None = None
