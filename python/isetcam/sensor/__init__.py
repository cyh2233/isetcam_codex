"""Sensor-related functions."""

from __future__ import annotations

import numpy as np

from .sensor_class import Sensor
from .sensor_get import sensor_get
from .sensor_set import sensor_set
from .sensor_from_file import sensor_from_file
from .sensor_compute import sensor_compute
from .sensor_photon_noise import sensor_photon_noise
from .sensor_add_noise import sensor_add_noise
from .sensor_to_file import sensor_to_file
from .sensor_create import sensor_create
from .sensor_snr import sensor_snr
from .sensor_snr_luxsec import sensor_snr_luxsec
from .sensor_crop import sensor_crop
from .sensor_plot import sensor_plot
from .sensor_ccm import sensor_ccm
from .sensor_dng_read import sensor_dng_read
from .sensor_show_image import sensor_show_image
from .sensor_rotate import sensor_rotate
from .sensor_show_cfa import sensor_show_cfa
from .sensor_stats import sensor_stats
from .sensor_clear_data import sensor_clear_data
from .sensor_iso_speed import sensor_iso_speed
from .sensor_resample_wave import sensor_resample_wave
from .sensor_rescale import sensor_rescale
from .sensor_gain_offset import sensor_gain_offset
from .sensor_dr import sensor_dr


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
    "sensor_photon_noise",
    "sensor_add_noise",
    "sensor_to_file",
    "sensor_create",
    "sensor_crop",
    "sensor_snr",
    "sensor_snr_luxsec",
    "sensor_plot",
    "sensor_ccm",
    "sensor_dng_read",
    "sensor_show_image",
    "sensor_show_cfa",
    "sensor_rotate",
    "sensor_stats",
    "sensor_clear_data",
    "sensor_iso_speed",
    "sensor_resample_wave",
    "sensor_rescale",
    "sensor_gain_offset",
    "sensor_dr",
]
