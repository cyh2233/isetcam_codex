"""Estimate sensor dynamic range in dB."""

from __future__ import annotations

from typing import Tuple

import numpy as np

from .sensor_class import Sensor
from .sensor_get import sensor_get


def sensor_dr(sensor: Sensor, integration_time: float | None = None) -> Tuple[float, float, float]:
    """Return dynamic range of ``sensor`` in dB.

    Parameters
    ----------
    sensor:
        Sensor object containing noise related attributes. Optional
        attributes ``dark_voltage`` (in volts/second), ``conversion_gain``
        (volts/electron), ``read_noise_electrons`` (electrons), ``gain_sd``
        (PRNU in percent), ``offset_sd`` (DSNU in volts) and ``voltage_swing``
        (maximum voltage) are used. When not present they default to zero for
        noise and unity for conversion gain and voltage swing.
    integration_time:
        Exposure time in seconds.  Defaults to ``sensor.exposure_time``.

    Returns
    -------
    tuple of float
        ``(dr_db, max_voltage, min_voltage)`` where ``dr_db`` is the dynamic
        range in decibels, ``max_voltage`` is the voltage swing minus the dark
        signal, and ``min_voltage`` is the standard deviation of the combined
        noise sources (dark current shot noise, read noise, DSNU and PRNU at
        ``max_voltage``).
    """

    if integration_time is None:
        integration_time = sensor_get(sensor, "exposure_time")
    integration_time = float(integration_time)
    if integration_time == 0:
        return float("nan"), float("nan"), float("nan")

    conv_gain = sensor_get(sensor, "conversion_gain")
    read_noise_e = sensor_get(sensor, "read_noise_electrons")
    gain_sd = sensor_get(sensor, "gain_sd") / 100.0
    offset_sd = sensor_get(sensor, "offset_sd")
    voltage_swing = sensor_get(sensor, "voltage_swing")

    dark_voltage = getattr(sensor, "dark_voltage", 0.0)
    dark_volts = dark_voltage * integration_time

    max_voltage = voltage_swing - dark_volts

    dark_electrons = dark_volts / conv_gain
    dk_var = dark_electrons * (conv_gain ** 2)
    rn_var = (read_noise_e * conv_gain) ** 2
    dsnu_var = offset_sd ** 2
    prnu_var = (gain_sd * max_voltage) ** 2

    min_voltage = float(np.sqrt(dk_var + rn_var + dsnu_var + prnu_var))

    if min_voltage == 0 or max_voltage <= 0:
        dr_db = float("inf")
    else:
        dr_db = float(10.0 * np.log10(max_voltage / min_voltage))

    return dr_db, float(max_voltage), min_voltage


__all__ = ["sensor_dr"]
