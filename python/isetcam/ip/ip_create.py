"""Create a :class:`VCImage` from a sensor and display."""

from __future__ import annotations

import numpy as np

from ..sensor import Sensor
from ..display import Display
from .vcimage_class import VCImage


def ip_create(sensor: Sensor, display: Display) -> VCImage:
    """Initialise a VCImage compatible with ``sensor`` and ``display``."""
    wave = sensor.wave if sensor.wave is not None else display.wave
    if wave is None:
        raise ValueError("Sensor or Display must define wavelength samples")

    if display.wave is not None and not np.array_equal(wave, display.wave):
        if len(wave) != len(display.wave):
            raise ValueError("Sensor and Display must have matching wavelengths")
        # adopt sensor.wave; assume display.spd is compatible

    rgb_shape = sensor.volts.shape + (3,)
    rgb = np.zeros(rgb_shape, dtype=float)
    name_parts = []
    if getattr(sensor, "name", None):
        name_parts.append(sensor.name)
    if getattr(display, "name", None):
        name_parts.append(display.name)
    name = "-".join(name_parts) if name_parts else None
    return VCImage(rgb=rgb, wave=wave, name=name)
