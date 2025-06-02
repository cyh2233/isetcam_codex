# mypy: ignore-errors
from __future__ import annotations

from typing import Sequence

import numpy as np

from ..sensor import Sensor


def cp_burst_ip(sensors: Sequence[Sensor], mode: str = "sum") -> np.ndarray:
    """Combine a sequence of sensor frames."""
    if not sensors:
        raise ValueError("sensors list is empty")
    stack = np.stack([s.volts for s in sensors], axis=0)
    mode = mode.lower()
    if mode == "sum":
        return stack.sum(axis=0)
    if mode == "longest":
        return stack[-1]
    raise ValueError("Unknown mode")
