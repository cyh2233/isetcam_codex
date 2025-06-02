# mypy: ignore-errors
"""Remove a color filter from a :class:`Sensor`."""

from __future__ import annotations

import numpy as np

from .sensor_class import Sensor


def sensor_delete_filter(sensor: Sensor, which_filter: int) -> Sensor:
    """Delete filter ``which_filter`` from ``sensor``.

    Parameters
    ----------
    sensor : Sensor
        Sensor instance containing ``filter_spectra`` and ``filter_names``.
    which_filter : int
        Index of the filter to remove (0-based).
    """
    if not hasattr(sensor, "filter_spectra"):
        raise AttributeError("sensor has no 'filter_spectra'")
    fs = np.asarray(sensor.filter_spectra, dtype=float)
    if which_filter < 0 or which_filter >= fs.shape[1]:
        raise IndexError("which_filter out of range")
    sensor.filter_spectra = np.delete(fs, which_filter, axis=1)

    names = list(getattr(sensor, "filter_names", []))
    if names and which_filter < len(names):
        del names[which_filter]
    sensor.filter_names = names
    return sensor


__all__ = ["sensor_delete_filter"]
