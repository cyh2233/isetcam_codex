"""Utilities for saving :class:`Sensor` objects to disk."""

from __future__ import annotations

from pathlib import Path

from scipy.io import savemat

from .sensor_class import Sensor


def sensor_to_file(sensor: Sensor, path: str | Path) -> None:
    """Save ``sensor`` to ``path`` as a MATLAB ``.mat`` file."""
    data = {
        "volts": sensor.volts,
        "exposure_time": sensor.exposure_time,
        "wave": sensor.wave,
    }
    if sensor.name is not None:
        data["name"] = sensor.name
    savemat(str(Path(path)), {"sensor": data})
