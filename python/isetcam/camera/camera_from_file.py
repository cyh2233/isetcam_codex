"""Load a :class:`Camera` from a MATLAB ``.mat`` file."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import numpy as np
from scipy.io import loadmat

from .camera_class import Camera
from ..sensor import Sensor
from ..opticalimage import OpticalImage


def _get_attr(obj: object, name: str):
    if isinstance(obj, dict):
        return obj.get(name)
    return getattr(obj, name, None)


def camera_from_file(
    path: str | Path,
    *,
    candidate_vars: Iterable[str] | None = None,
) -> Camera:
    """Load ``path`` and return a :class:`Camera`.

    Parameters
    ----------
    path:
        MAT-file containing a camera structure.
    candidate_vars:
        Optional sequence of variable names to search for. Defaults to
        ``('camera',)``.
    """
    if candidate_vars is None:
        candidate_vars = ("camera",)

    mat = loadmat(str(Path(path)), squeeze_me=True, struct_as_record=False)

    cam_struct = None
    for key in candidate_vars:
        if key in mat:
            cam_struct = mat[key]
            break
    if cam_struct is None:
        raise KeyError("No camera structure found in file")

    sensor_struct = _get_attr(cam_struct, "sensor")
    if sensor_struct is None:
        raise KeyError("Camera structure missing sensor")
    oi_struct = _get_attr(cam_struct, "optical_image")
    if oi_struct is None:
        raise KeyError("Camera structure missing optical image")

    # Sensor fields
    s_volts = np.asarray(_get_attr(sensor_struct, "volts"))
    s_exp_time = float(_get_attr(sensor_struct, "exposure_time"))
    s_wave = _get_attr(sensor_struct, "wave")
    if s_wave is not None:
        s_wave = np.asarray(s_wave).reshape(-1)
    s_name = _get_attr(sensor_struct, "name")
    if isinstance(s_name, np.ndarray):
        s_name = str(s_name.squeeze())
    sensor = Sensor(volts=s_volts, exposure_time=s_exp_time, wave=s_wave, name=s_name)

    # Optical image fields
    oi_photons = np.asarray(_get_attr(oi_struct, "photons"))
    oi_wave = _get_attr(oi_struct, "wave")
    if oi_wave is not None:
        oi_wave = np.asarray(oi_wave).reshape(-1)
    oi_name = _get_attr(oi_struct, "name")
    if isinstance(oi_name, np.ndarray):
        oi_name = str(oi_name.squeeze())
    oi = OpticalImage(photons=oi_photons, wave=oi_wave, name=oi_name)

    name = _get_attr(cam_struct, "name")
    if isinstance(name, np.ndarray):
        name = str(name.squeeze())

    return Camera(sensor=sensor, optical_image=oi, name=name)
