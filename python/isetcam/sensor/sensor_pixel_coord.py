# mypy: ignore-errors
"""Return pixel center coordinates for a :class:`Sensor`."""

from __future__ import annotations

import numpy as np

from .sensor_class import Sensor


def sensor_pixel_coord(sensor: Sensor) -> tuple[np.ndarray, np.ndarray]:
    """Return ``(x, y)`` coordinate arrays for pixel centers.

    The coordinates are measured relative to the sensor centre.  When
    ``sensor`` has ``pixel_size`` defined the coordinates are returned in
    metres, otherwise they are in pixel units.  Any accumulated jiggle
    offsets stored on ``sensor`` are applied.
    """

    rows, cols = sensor.volts.shape[:2]
    pixel_size = float(getattr(sensor, "pixel_size", 1.0))
    cx = (cols - 1) / 2.0
    cy = (rows - 1) / 2.0

    x = (np.arange(cols) - cx) * pixel_size
    y = (np.arange(rows) - cy) * pixel_size

    X, Y = np.meshgrid(x, y)

    dx = float(getattr(sensor, "jiggle_dx", 0)) * pixel_size
    dy = float(getattr(sensor, "jiggle_dy", 0)) * pixel_size
    X += dx
    Y += dy
    return X, Y


__all__ = ["sensor_pixel_coord"]
