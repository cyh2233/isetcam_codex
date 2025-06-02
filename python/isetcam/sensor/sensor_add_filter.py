# mypy: ignore-errors
"""Append a color filter to a :class:`Sensor`."""

from __future__ import annotations

from pathlib import Path
import numpy as np
from scipy.io import loadmat

from .sensor_class import Sensor


def sensor_add_filter(sensor: Sensor, filter_path: str | Path) -> Sensor:
    """Load ``filter_path`` and append its data to ``sensor``.

    The filter spectrum is interpolated to ``sensor.wave`` and appended to
    ``sensor.filter_spectra``. The corresponding filter name from the file is
    appended to ``sensor.filter_names``.
    """
    mat = loadmat(str(Path(filter_path)), squeeze_me=True, struct_as_record=False)
    data = np.asarray(mat["data"], dtype=float)
    src_wave = np.asarray(mat["wavelength"], dtype=float).reshape(-1)
    names = mat.get("filterNames")
    if names is None:
        name = Path(filter_path).stem
    else:
        name = str(np.atleast_1d(names)[0])

    column = data[:, 0] if data.ndim > 1 else data.reshape(-1)
    wave = np.asarray(sensor.wave, dtype=float)
    column = np.interp(wave, src_wave, column, left=0.0, right=0.0)
    column = column.reshape(-1, 1)

    if hasattr(sensor, "filter_spectra"):
        fs = np.asarray(sensor.filter_spectra, dtype=float)
        if fs.shape[0] != column.shape[0]:
            raise ValueError("filter length mismatch with sensor.wave")
        sensor.filter_spectra = np.column_stack((fs, column))
    else:
        sensor.filter_spectra = column

    if hasattr(sensor, "filter_names"):
        sensor.filter_names = list(sensor.filter_names) + [name]
    else:
        sensor.filter_names = [name]

    return sensor


__all__ = ["sensor_add_filter"]
