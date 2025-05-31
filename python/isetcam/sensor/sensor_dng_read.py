"""Load raw data from a DNG file into a :class:`Sensor`."""

from __future__ import annotations

from pathlib import Path

import numpy as np

try:  # pragma: no cover - optional dependency
    import rawpy  # type: ignore
except Exception:  # pragma: no cover - library may not be present
    rawpy = None  # type: ignore

from ..io import dng_read
from .sensor_class import Sensor


def sensor_dng_read(path: str | Path) -> Sensor:
    """Read ``path`` as a DNG image and return a :class:`Sensor`.

    The raw pixel data are stored in ``sensor.volts`` and common metadata
    such as ISO speed, exposure time, orientation and black level are stored
    as attributes on the returned object when available.
    """
    if rawpy is None:  # pragma: no cover - dependency missing
        raise RuntimeError("rawpy library is not available")

    p = Path(path)

    # Raw sensor values
    data = dng_read(p)

    # Extract metadata using rawpy
    with rawpy.imread(str(p)) as raw:
        meta = raw.metadata
        iso_speed = getattr(meta, "iso_speed", None)
        exposure = getattr(meta, "exposure", None)
        orientation = getattr(meta, "orientation", None)
        black_level = getattr(meta, "black_level_per_channel", None)

    exposure_time = float(exposure) if exposure is not None else 0.0
    sensor = Sensor(volts=data.astype(float), exposure_time=exposure_time, name=p.name)

    if iso_speed is not None:
        sensor.iso_speed = iso_speed
    if orientation is not None:
        sensor.orientation = orientation
    if black_level is not None:
        sensor.black_level = np.asarray(black_level).reshape(-1)

    return sensor
