# mypy: ignore-errors
"""Replace an existing color filter in a :class:`Sensor`."""

from __future__ import annotations

from pathlib import Path
import numpy as np
from scipy.io import loadmat

from .sensor_class import Sensor


def sensor_replace_filter(sensor: Sensor, which_filter: int, new_filter_file: str | Path) -> Sensor:
    """Replace filter ``which_filter`` with data from ``new_filter_file``."""
    if not hasattr(sensor, "filter_spectra"):
        raise AttributeError("sensor has no 'filter_spectra'")
    fs = np.asarray(sensor.filter_spectra, dtype=float)
    if which_filter < 0 or which_filter >= fs.shape[1]:
        raise IndexError("which_filter out of range")

    mat = loadmat(str(Path(new_filter_file)), squeeze_me=True, struct_as_record=False)
    data = np.asarray(mat["data"], dtype=float)
    src_wave = np.asarray(mat["wavelength"], dtype=float).reshape(-1)
    names = mat.get("filterNames")
    if names is None:
        name = Path(new_filter_file).stem
    else:
        name = str(np.atleast_1d(names)[0])

    column = data[:, 0] if data.ndim > 1 else data.reshape(-1)
    wave = np.asarray(sensor.wave, dtype=float)
    column = np.interp(wave, src_wave, column, left=0.0, right=0.0)

    if column.size != fs.shape[0]:
        raise ValueError("filter length mismatch with sensor.wave")
    fs[:, which_filter] = column
    sensor.filter_spectra = fs

    names_list = list(getattr(sensor, "filter_names", []))
    while len(names_list) < fs.shape[1]:
        names_list.append("")
    names_list[which_filter] = name
    sensor.filter_names = names_list

    return sensor


__all__ = ["sensor_replace_filter"]
