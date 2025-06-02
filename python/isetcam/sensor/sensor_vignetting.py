# mypy: ignore-errors
"""Compute pixel vignetting map for a sensor.

This is a very small subset of the original MATLAB implementation.  When
``pv_flag`` is ``0`` or ``"skip"`` a unity map is attached to ``sensor`` as the
``etendue`` attribute.  Numeric ``pv_flag`` values are interpreted as

``1`` - bare sensor (no microlens)
``2`` - sensor with centered microlens
``3`` - sensor with an optimally placed microlens

Passing ``"microlens"`` selects the centered microlens case.  The returned
``sensor`` will contain an ``etendue`` attribute holding the per pixel
vignetting map.
"""

from __future__ import annotations

import numpy as np

from .sensor_class import Sensor


def sensor_vignetting(
    sensor: Sensor, pv_flag: int | str = 0, n_angles: int = 5
) -> Sensor:
    """Attach vignetting (etendue) information to ``sensor``.

    This is a simplified version of the MATLAB ``sensorVignetting`` function.
    When ``pv_flag`` is ``0`` or ``"skip"`` a unity etendue map matching the
    voltage image size is stored on ``sensor`` as attribute ``etendue``.  When a
    microlens option is chosen the map is approximated from the microlens focal
    length and the sensor pixel size.
    """
    flag = pv_flag
    if isinstance(flag, str):
        flag = flag.lower()

    if flag in (0, "skip", None):
        sensor.etendue = np.ones_like(sensor.volts, dtype=float)
        return sensor

    if flag in (1, "bare", "no microlens"):
        method = "bare"
    elif flag in (2, 3, "microlens", "centered", "optimal"):
        method = "microlens"
    else:
        raise ValueError(f"Unknown pv_flag '{pv_flag}'")

    rows, cols = sensor.volts.shape[:2]
    cx = (cols - 1) / 2.0
    cy = (rows - 1) / 2.0

    pixel_size = float(getattr(sensor, "pixel_size", 1e-6))
    x = (np.arange(cols) - cx) * pixel_size
    y = (np.arange(rows) - cy) * pixel_size
    r = np.sqrt(x[None, :] ** 2 + y[:, None] ** 2)

    ml_fnumber = float(getattr(sensor, "microlens_f_number", 2.8))
    focal_length = ml_fnumber * pixel_size
    theta = np.arctan(r / focal_length)

    if method == "bare":
        etendue = np.cos(theta) ** 4
    else:
        etendue = np.cos(theta) ** 2

    sensor.etendue = etendue.astype(float)
    return sensor


__all__ = ["sensor_vignetting"]
