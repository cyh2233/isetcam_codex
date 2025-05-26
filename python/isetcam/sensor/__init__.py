"""Sensor-related functions."""

from __future__ import annotations

import numpy as np

from .sensor_class import Sensor
from .sensor_get import sensor_get
from .sensor_set import sensor_set
from .sensor_from_file import sensor_from_file
from .sensor_compute import sensor_compute
from .sensor_to_file import sensor_to_file
from .sensor_create import sensor_create


def get_volts(sensor: Sensor) -> np.ndarray:
    """Return the voltage data from ``sensor``."""
    return sensor.volts


def set_volts(sensor: Sensor, volts: np.ndarray) -> None:
    """Set the voltage data for ``sensor``."""
    sensor.volts = np.asarray(volts)


def get_exposure_time(sensor: Sensor) -> float:
    """Return the exposure time for ``sensor``."""
    return sensor.exposure_time


def set_exposure_time(sensor: Sensor, exposure_time: float) -> None:
    """Set the exposure time for ``sensor``."""
    sensor.exposure_time = float(exposure_time)


def get_n_wave(sensor: Sensor) -> int:
    """Return the number of wavelength samples in ``sensor``."""
    return len(sensor.wave)


__all__ = [
    "Sensor",
    "get_volts",
    "set_volts",
    "get_exposure_time",
    "set_exposure_time",
    "get_n_wave",
    "sensor_get",
    "sensor_set",
    "sensor_from_file",
    "sensor_compute",
    "sensor_to_file",
    "sensor_create",
]
