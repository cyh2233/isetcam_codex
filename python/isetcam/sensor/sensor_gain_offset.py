# mypy: ignore-errors
"""Apply analog gain and offset to sensor voltages."""

from __future__ import annotations

from .sensor_class import Sensor


def sensor_gain_offset(sensor: Sensor, gain: float = 1.0, offset: float = 0.0) -> Sensor:
    """Apply multiplicative ``gain`` and additive ``offset`` to ``sensor.volts``."""

    sensor.volts = sensor.volts * float(gain) + float(offset)
    return sensor


__all__ = ["sensor_gain_offset"]
