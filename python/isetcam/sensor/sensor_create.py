# mypy: ignore-errors
"""Factory function for :class:`Sensor` objects."""

from __future__ import annotations

from typing import Optional

import numpy as np

from .sensor_class import Sensor

_DEF_PIXEL_SIZE = 2.8e-6  # meters
_DEF_EXPOSURE = 0.01  # seconds


def sensor_create(kind: str = "bayer", wave: Optional[np.ndarray] = None) -> Sensor:
    """Create a simple :class:`Sensor` by ``kind``.

    Parameters
    ----------
    kind:
        Type of sensor to create. Only ``'bayer'`` is currently supported.
    wave:
        Optional wavelength sampling for the sensor's spectral properties.
    """
    flag = kind.lower().replace(" ", "")
    if flag != "bayer":
        raise ValueError(f"Unknown sensor type '{kind}'")

    volts = np.zeros((1, 1), dtype=float)
    s = Sensor(volts=volts, exposure_time=_DEF_EXPOSURE, wave=wave, name=kind)

    # Default quantum efficiency and pixel size information
    s.qe = np.ones(s.wave.size, dtype=float)
    s.pixel_size = float(_DEF_PIXEL_SIZE)
    return s
