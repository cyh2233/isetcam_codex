"""Sensor SNR as a function of photometric exposure (lux-seconds)."""

from __future__ import annotations

from typing import Tuple

import numpy as np

from .sensor_class import Sensor
from .sensor_get import sensor_get
from .sensor_snr import sensor_snr


def sensor_snr_luxsec(sensor: Sensor) -> Tuple[np.ndarray, np.ndarray]:
    """Return sensor SNR versus photometric exposure.

    The conversion from volts to lux-seconds is controlled by the optional
    ``volts_per_lux_sec`` attribute on ``sensor``.  When absent a value of ``1``
    is assumed.
    """

    snr, volts, *_ = sensor_snr(sensor)

    v_per_ls = getattr(sensor, "volts_per_lux_sec", 1.0)
    n_colors = sensor_get(sensor, "ncolors")

    luxsec = np.zeros((volts.size, n_colors), dtype=float)
    if np.isscalar(v_per_ls):
        for i in range(n_colors):
            luxsec[:, i] = volts / v_per_ls
    else:
        v_per_ls = np.asarray(v_per_ls, dtype=float)
        if v_per_ls.size != n_colors:
            raise ValueError("volts_per_lux_sec length must match number of colors")
        for i in range(n_colors):
            luxsec[:, i] = volts / v_per_ls[i]

    return snr, luxsec


__all__ = ["sensor_snr_luxsec"]

