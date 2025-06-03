# mypy: ignore-errors
"""Create a centered photodiode for a :class:`Sensor`."""

from __future__ import annotations

import numpy as np

from .pixel_class import Pixel
from ..sensor.sensor_class import Sensor


def pixel_center_fill_pd(sensor: Sensor, fill_factor: float) -> Sensor:
    """Attach a centered photodiode ``Pixel`` to ``sensor``.

    Parameters
    ----------
    sensor:
        Sensor to update.
    fill_factor:
        Desired photodiode fill factor ``0`` to ``1`` relative to the pixel
        pitch stored on ``sensor`` as ``pixel_size``.

    Returns
    -------
    Sensor
        ``sensor`` updated with a ``pixel`` attribute describing the
        photodiode. The voltage data are scaled by ``fill_factor``.
    """

    if not 0.0 <= fill_factor <= 1.0:
        raise ValueError("fill_factor must be between 0 and 1")

    pixel_size = float(getattr(sensor, "pixel_size", 1.0))
    pd_side = np.sqrt(fill_factor) * pixel_size
    well_capacity = float(getattr(sensor, "well_capacity", 0.0))

    sensor.pixel = Pixel(
        width=pd_side,
        height=pd_side,
        well_capacity=well_capacity,
        fill_factor=float(fill_factor),
    )

    sensor.volts = np.asarray(sensor.volts, dtype=float) * float(fill_factor)
    return sensor


__all__ = ["pixel_center_fill_pd"]
