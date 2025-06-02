"""Compute pixel vignetting map for a sensor."""

from __future__ import annotations

import numpy as np

from .sensor_class import Sensor


def sensor_vignetting(
    sensor: Sensor, pv_flag: int | str = 0, n_angles: int = 5
) -> Sensor:
    """Attach vignetting (etendue) information to ``sensor``.

    This is a simplified version of the MATLAB ``sensorVignetting`` function.
    When ``pv_flag`` is ``0`` or ``"skip"`` a unity etendue map matching the
    voltage image size is stored on ``sensor`` as attribute ``etendue``.
    Other ``pv_flag`` values are not implemented and will raise
    ``NotImplementedError``.
    """
    if pv_flag in (0, "skip", None):
        sensor.etendue = np.ones_like(sensor.volts, dtype=float)
        return sensor

    raise NotImplementedError("Microlens vignetting not implemented in Python")


__all__ = ["sensor_vignetting"]
