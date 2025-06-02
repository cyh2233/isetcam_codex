# mypy: ignore-errors
"""Compute ISO speed from sensor noise parameters using SNR=10 criterion."""

from __future__ import annotations

import numpy as np

from .sensor_class import Sensor
from .sensor_get import sensor_get


def sensor_iso_speed(sensor: Sensor) -> float:
    """Return the ISO speed for ``sensor`` using the SNR=10 method."""
    conv_gain = sensor_get(sensor, "conversion_gain")
    read_noise = sensor_get(sensor, "read_noise_electrons")
    gain_sd = sensor_get(sensor, "gain_sd") / 100.0
    offset_sd = sensor_get(sensor, "offset_sd")

    dsnu = offset_sd / conv_gain

    a = 100.0 * gain_sd ** 2 - 1.0
    b = 100.0
    c = 100.0 * (read_noise ** 2 + dsnu ** 2)

    if a >= 0:
        return float("inf")

    disc = b ** 2 - 4.0 * a * c
    if disc < 0:
        return float("inf")

    sqrt_disc = float(np.sqrt(disc))
    e1 = (-b + sqrt_disc) / (2.0 * a)
    e2 = (-b - sqrt_disc) / (2.0 * a)
    electrons = e1 if e1 > 0 else e2
    if electrons <= 0:
        return float("inf")

    v_per_ls = getattr(sensor, "volts_per_lux_sec", 1.0)
    luxsec = electrons / (conv_gain * v_per_ls)

    return 10.0 / luxsec
