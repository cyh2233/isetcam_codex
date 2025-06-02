# mypy: ignore-errors
"""Extract a rectangular ROI from a :class:`Sensor`."""

from __future__ import annotations

from typing import Sequence, Tuple

import numpy as np

from .sensor_class import Sensor
from ..ie_clip import ie_clip


def sensor_roi(sensor: Sensor, rect: Sequence[int]) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return ROI volts and indices from ``sensor``.

    Parameters
    ----------
    sensor : Sensor
        Sensor object containing voltage data.
    rect : sequence of int
        ``(x, y, width, height)`` rectangle using 0-based indexing. Values
        outside the sensor bounds are clipped similar to MATLAB.

    Returns
    -------
    tuple of np.ndarray
        ``(roi_volts, rows, cols)`` where ``rows`` and ``cols`` are the
        index arrays for the selected region.
    """

    if len(rect) != 4:
        raise ValueError("rect must have four elements (x, y, width, height)")

    x, y, w, h = [int(v) for v in rect]
    if w <= 0 or h <= 0:
        raise ValueError("width and height must be positive")

    volts = np.asarray(sensor.volts)
    nrows, ncols = volts.shape[:2]

    row_idx = np.arange(y, y + h, dtype=int)
    col_idx = np.arange(x, x + w, dtype=int)

    row_idx = ie_clip(row_idx, 0, nrows - 1).astype(int)
    col_idx = ie_clip(col_idx, 0, ncols - 1).astype(int)

    roi_volts = volts[np.ix_(row_idx, col_idx)]
    return roi_volts, row_idx, col_idx


__all__ = ["sensor_roi"]
