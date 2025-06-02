# mypy: ignore-errors
"""Resize a Sensor to achieve a desired field of view."""

from __future__ import annotations

import math
from typing import Sequence

import numpy as np

from .sensor_class import Sensor
from .sensor_clear_data import sensor_clear_data
from ..optics import Optics
from ..opticalimage import OpticalImage


def _cfa_block_size(sensor: Sensor) -> tuple[int, int]:
    """Return the CFA block size for ``sensor`` if available."""
    letters = getattr(sensor, "filter_color_letters", None)
    if letters is None:
        return 1, 1

    arr: np.ndarray | None
    if isinstance(letters, str):
        size = int(math.sqrt(len(letters)))
        arr = np.array(list(letters)).reshape(size, size) if size * size == len(letters) else None
    else:
        arr = np.asarray(letters)
        if arr.ndim == 1:
            size = int(math.sqrt(arr.size))
            arr = arr.reshape(size, size) if size * size == arr.size else None
        elif arr.ndim != 2:
            arr = None
    if arr is None:
        return 1, 1
    return int(arr.shape[0]), int(arr.shape[1])


def sensor_set_size_to_fov(sensor: Sensor, new_fov: float | Sequence[float], oi: OpticalImage | Optics) -> Sensor:
    """Adjust ``sensor`` so its field of view matches ``new_fov``.

    The optics focal length is taken from ``oi.optics`` when present or from
    ``oi`` itself if it is an :class:`Optics` instance. The voltage data are
    replaced with zeros of the new size and any cached attributes are removed.
    """
    optics = getattr(oi, "optics", oi)
    flength = getattr(optics, "f_length", None)
    if flength is None:
        raise ValueError("oi must supply optics with f_length")
    flength = float(flength)

    volts = np.asarray(sensor.volts)
    rows, cols = volts.shape[:2]
    n_channels = volts.shape[2] if volts.ndim == 3 else 1

    pixel_size = float(getattr(sensor, "pixel_size", 1e-6))
    cur_width = cols * pixel_size
    cur_height = rows * pixel_size

    if np.isscalar(new_fov):
        hfov = float(new_fov)
        desired_width = 2 * flength * math.tan(math.radians(hfov) / 2.0)
        scale = desired_width / cur_width
        new_rows = int(round(rows * scale))
        new_cols = int(round(cols * scale))
    else:
        fov = np.asarray(new_fov, dtype=float).reshape(-1)
        if fov.size != 2:
            raise ValueError("new_fov must be scalar or a length-2 sequence")
        hfov, vfov = float(fov[0]), float(fov[1])
        desired_width = 2 * flength * math.tan(math.radians(hfov) / 2.0)
        desired_height = 2 * flength * math.tan(math.radians(vfov) / 2.0)
        new_cols = int(round(cols * desired_width / cur_width))
        new_rows = int(round(rows * desired_height / cur_height))

    if new_rows <= 0:
        new_rows = 1
    if new_cols <= 0:
        new_cols = 1

    block_r, block_c = _cfa_block_size(sensor)
    new_rows = int(math.ceil(new_rows / block_r)) * block_r
    new_cols = int(math.ceil(new_cols / block_c)) * block_c
    new_rows = max(new_rows, block_r)
    new_cols = max(new_cols, block_c)

    shape = (new_rows, new_cols) if n_channels == 1 else (new_rows, new_cols, n_channels)
    sensor.volts = np.zeros(shape, dtype=float)

    sensor_clear_data(sensor)
    return sensor


__all__ = ["sensor_set_size_to_fov"]
