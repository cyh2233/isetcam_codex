# mypy: ignore-errors
"""Compute sensor response one waveband at a time."""

from __future__ import annotations

from typing import Iterable, Sequence

import numpy as np

from ..opticalimage import OpticalImage
from .sensor_class import Sensor


def sensor_wb_compute(sensor: Sensor, ois: Iterable[OpticalImage]) -> Sensor:
    """Accumulate sensor response from ``ois``.

    Each optical image in ``ois`` may contain one or more wavelength bands.
    The response for each band is integrated and summed into ``sensor.volts``.

    Parameters
    ----------
    sensor:
        Destination sensor object. ``sensor.volts`` provides the output size
        and is overwritten with the computed voltages.
    ois:
        Iterable of optical images ordered by wavelength.

    Returns
    -------
    Sensor
        The input ``sensor`` with its ``volts`` attribute updated with the
        summed response.
    """
    wave = np.asarray(sensor.wave)
    qe = getattr(sensor, "qe", np.ones_like(wave, dtype=float))
    volts = np.zeros_like(sensor.volts, dtype=float)

    oi_list: Sequence[OpticalImage] = list(ois)

    for oi in oi_list:
        photons = np.asarray(oi.photons)
        oi_wave = np.asarray(oi.wave)
        if photons.ndim == 2:
            photons = photons[:, :, np.newaxis]
        for band in range(photons.shape[2]):
            w = oi_wave[band]
            idx = int(np.argmin(np.abs(wave - w)))
            volts += (
                photons[:, :, band].astype(float)
                * float(qe[idx])
                * float(sensor.exposure_time)
            )

    sensor.volts = volts

    if oi_list:
        last = oi_list[-1]
        if getattr(last, "name", None):
            sensor.name = f"wb-{last.name}"
    return sensor


__all__ = ["sensor_wb_compute"]
