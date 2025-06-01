"""Resize sensor voltage data and adjust pixel size metadata."""

from __future__ import annotations

from typing import Sequence

import numpy as np
from scipy.ndimage import zoom as nd_zoom

from .sensor_class import Sensor


def sensor_rescale(sensor: Sensor, row_col: Sequence[int], sensor_size: Sequence[float]) -> Sensor:
    """Return ``sensor`` resized to ``row_col`` pixels.

    Parameters
    ----------
    sensor : Sensor
        Input sensor to rescale.
    row_col : sequence of int
        Desired ``(rows, cols)`` for the output voltage image.
    sensor_size : sequence of float
        Physical size of the sensor in meters as ``(height, width)``.
    """

    rows, cols = [int(v) for v in row_col]
    if rows <= 0 or cols <= 0:
        raise ValueError("row_col must contain positive integers")

    volts = np.asarray(sensor.volts, dtype=float)
    zoom_factors = (rows / volts.shape[0], cols / volts.shape[1])
    resized = nd_zoom(volts, zoom_factors, order=1)

    out = Sensor(
        volts=resized,
        wave=sensor.wave,
        exposure_time=sensor.exposure_time,
        name=sensor.name,
    )

    if isinstance(sensor_size, Sequence):
        if len(sensor_size) == 2:
            height, width = float(sensor_size[0]), float(sensor_size[1])
        else:
            height = width = float(sensor_size[0])
    else:
        height = width = float(sensor_size)

    out.pixel_size = (height / rows + width / cols) / 2.0
    return out


__all__ = ["sensor_rescale"]
