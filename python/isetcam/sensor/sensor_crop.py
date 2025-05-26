"""Crop volts from a :class:`Sensor` while preserving CFA alignment."""

from __future__ import annotations

from typing import Sequence

import numpy as np

from .sensor_class import Sensor


def sensor_crop(sensor: Sensor, rect: Sequence[int]) -> Sensor:
    """Return a new sensor cropped to ``rect``.

    The crop rectangle is given as ``(x, y, width, height)`` using 0-based
    indexing. To preserve the 2x2 CFA pattern alignment the ``x`` and ``y``
    coordinates as well as ``width`` and ``height`` must be even numbers.
    ``ValueError`` is raised if the rectangle lies outside the sensor bounds
    or violates the CFA alignment.
    """

    if len(rect) != 4:
        raise ValueError("rect must have four elements (x, y, width, height)")

    x, y, w, h = [int(v) for v in rect]
    if w <= 0 or h <= 0:
        raise ValueError("width and height must be positive")

    volts = np.asarray(sensor.volts)
    s_height, s_width = volts.shape[:2]

    if x < 0 or y < 0 or x + w > s_width or y + h > s_height:
        raise ValueError("rect is outside the sensor bounds")

    if (x % 2) or (y % 2) or (w % 2) or (h % 2):
        raise ValueError("rect must align with the 2x2 CFA pattern")

    cropped = volts[y : y + h, x : x + w, ...].copy()
    out = Sensor(
        volts=cropped,
        wave=sensor.wave,
        exposure_time=sensor.exposure_time,
        name=sensor.name,
    )
    out.crop_rect = (x, y, w, h)
    out.full_size = (s_height, s_width)
    return out
