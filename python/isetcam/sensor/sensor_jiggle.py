# mypy: ignore-errors
"""Shift sensor voltage data by integer pixel offsets."""

from __future__ import annotations

import numpy as np

from .sensor_class import Sensor


def sensor_jiggle(sensor: Sensor, dx: int, dy: int, fill: float = 0) -> Sensor:
    """Return ``sensor`` shifted by ``dx`` and ``dy`` pixels.

    Positive ``dx`` values move the image to the right and positive ``dy``
    values move it down.  Areas exposed by the shift are filled with
    ``fill``.  The jiggle offsets are accumulated on the returned sensor
    using the ``jiggle_dx`` and ``jiggle_dy`` attributes so that
    :func:`sensor_pixel_coord` reflects the new pixel positions.
    """

    volts = np.asarray(sensor.volts)
    h, w = volts.shape[:2]
    shifted = np.full_like(volts, fill, dtype=volts.dtype)

    if abs(dx) < w and abs(dy) < h:
        if dx >= 0:
            src_x = slice(0, w - dx)
            dst_x = slice(dx, dx + (w - dx))
        else:
            src_x = slice(-dx, w)
            dst_x = slice(0, w + dx)

        if dy >= 0:
            src_y = slice(0, h - dy)
            dst_y = slice(dy, dy + (h - dy))
        else:
            src_y = slice(-dy, h)
            dst_y = slice(0, h + dy)

        shifted[dst_y, dst_x, ...] = volts[src_y, src_x, ...]

    out = Sensor(
        volts=shifted,
        wave=sensor.wave,
        exposure_time=sensor.exposure_time,
        name=sensor.name,
    )

    for attr in ("pixel_size", "filter_color_letters", "n_colors"):
        if hasattr(sensor, attr):
            setattr(out, attr, getattr(sensor, attr))

    out.jiggle_dx = getattr(sensor, "jiggle_dx", 0) + int(dx)
    out.jiggle_dy = getattr(sensor, "jiggle_dy", 0) + int(dy)
    return out


__all__ = ["sensor_jiggle"]
