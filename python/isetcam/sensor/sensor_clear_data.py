# mypy: ignore-errors
"""Utility to remove optional attributes from a Sensor."""

from __future__ import annotations

from .sensor_class import Sensor

# Attributes that may be attached to Sensor instances by various helpers
# or user interfaces. These are removed by :func:`sensor_clear_data`.
_OPTIONAL_ATTRS = [
    "offset_fpn_image",
    "gain_fpn_image",
    "data",
    "crop_rect",
    "full_size",
]


def sensor_clear_data(sensor: Sensor) -> Sensor:
    """Remove cached or optional attributes from ``sensor``.

    Parameters
    ----------
    sensor : Sensor
        Sensor object to clean.

    Returns
    -------
    Sensor
        The same ``sensor`` instance with extraneous attributes removed.
    """
    for attr in _OPTIONAL_ATTRS:
        if hasattr(sensor, attr):
            delattr(sensor, attr)
    if getattr(sensor, "name", None) is None:
        sensor.name = ""
    return sensor


__all__ = ["sensor_clear_data"]
