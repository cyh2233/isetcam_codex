# mypy: ignore-errors
"""Factory function for :class:`Camera` objects."""

from __future__ import annotations

from typing import Optional

import numpy as np

from .camera_class import Camera
from ..sensor import sensor_create, Sensor
from ..optics import optics_create, Optics
from ..opticalimage import OpticalImage


def camera_create(sensor: Optional[Sensor] = None,
                  optics: Optional[Optics] = None,
                  name: Optional[str] = None) -> Camera:
    """Create a :class:`Camera` composed of a sensor and optics."""
    if sensor is None:
        sensor = sensor_create()
    if optics is None:
        optics = optics_create()

    if sensor.wave is not None:
        wave = sensor.wave
    else:
        wave = optics.wave

    photons = np.zeros((1, 1, wave.size), dtype=float)
    oi = OpticalImage(photons=photons, wave=wave, name=name)

    cam = Camera(sensor=sensor, optical_image=oi, name=name)
    # attach the optics instance for reference
    cam.optics = optics
    return cam
