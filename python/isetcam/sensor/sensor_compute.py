"""Compute sensor response from an optical image."""

from __future__ import annotations

import numpy as np

from ..opticalimage import OpticalImage
from .sensor_class import Sensor


def sensor_compute(sensor: Sensor, oi: OpticalImage) -> Sensor:
    """Integrate photons in ``oi`` to produce sensor volts.

    Parameters
    ----------
    sensor : Sensor
        Sensor dataclass which may optionally contain a ``qe`` attribute
        giving the quantum efficiency for each wavelength sample.
    oi : OpticalImage
        Optical image providing photon data.

    Returns
    -------
    Sensor
        ``sensor`` with its ``volts`` attribute set to the integrated
        response.
    """
    if oi.photons.shape[-1] != sensor.wave.size:
        raise ValueError("OpticalImage and Sensor must have matching wavelengths")

    qe = getattr(sensor, "qe", None)
    if qe is None:
        qe = np.ones(sensor.wave.size, dtype=float)
    else:
        qe = np.asarray(qe, dtype=float)
        if qe.size != sensor.wave.size:
            raise ValueError("sensor.qe length must match sensor.wave")

    electrons = (oi.photons * qe).sum(axis=2) * float(sensor.exposure_time)
    sensor.volts = electrons
    return sensor

