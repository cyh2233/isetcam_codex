# mypy: ignore-errors
"""Load a :class:`Sensor` from a MATLAB ``.mat`` file."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import numpy as np
from scipy.io import loadmat

from .sensor_class import Sensor


def _get_attr(obj: object, name: str):
    if isinstance(obj, dict):
        return obj.get(name)
    return getattr(obj, name, None)


def sensor_from_file(path: str | Path, *, candidate_vars: Iterable[str] | None = None) -> Sensor:  # noqa: E501
    """Load ``path`` and return a :class:`Sensor`.

    Parameters
    ----------
    path:
        MAT-file containing a sensor structure.
    candidate_vars:
        Optional sequence of variable names to search for. Defaults to
        ``('sensor', 'isa', 'isa_')``.
    """
    if candidate_vars is None:
        candidate_vars = ("sensor", "isa", "isa_")

    mat = loadmat(str(Path(path)), squeeze_me=True, struct_as_record=False)

    sensor_struct = None
    for key in candidate_vars:
        if key in mat:
            sensor_struct = mat[key]
            break
    if sensor_struct is None:
        raise KeyError("No sensor structure found in file")

    volts = np.asarray(_get_attr(sensor_struct, "volts"))
    exposure_time = float(_get_attr(sensor_struct, "exposure_time"))
    wave = _get_attr(sensor_struct, "wave")
    if wave is not None:
        wave = np.asarray(wave).reshape(-1)
    name = _get_attr(sensor_struct, "name")
    if isinstance(name, np.ndarray):
        name = str(name.squeeze())

    return Sensor(volts=volts, exposure_time=exposure_time, wave=wave, name=name)
