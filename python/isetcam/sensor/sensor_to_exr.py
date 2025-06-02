# mypy: ignore-errors
"""Save Sensor voltage data to an OpenEXR file."""

from __future__ import annotations

from pathlib import Path
from typing import Dict

import numpy as np

from .sensor_class import Sensor
from ..io import openexr_write


def _volts_to_channels(volts: np.ndarray) -> Dict[str, np.ndarray]:
    """Return mapping of channel names to planes of ``volts``."""
    arr = np.asarray(volts, dtype=np.float32)
    if arr.ndim == 2:
        arr = arr[:, :, np.newaxis]
    if arr.ndim != 3:
        raise ValueError("volts must be 2-D or 3-D array")
    n_chan = arr.shape[2]
    if n_chan == 1:
        names = ["Y"]
    elif n_chan == 3:
        names = ["R", "G", "B"]
    elif n_chan == 4:
        names = ["R", "G", "B", "A"]
    else:
        names = [f"channel{i}" for i in range(n_chan)]
    return {name: arr[:, :, i] for i, name in enumerate(names)}


def sensor_to_exr(sensor: Sensor, path: str | Path) -> None:
    """Save ``sensor`` voltage data to ``path`` as an OpenEXR image."""
    channels = _volts_to_channels(sensor.volts)
    openexr_write(path, channels)


__all__ = ["sensor_to_exr"]
