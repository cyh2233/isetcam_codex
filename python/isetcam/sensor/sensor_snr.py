"""Estimate sensor SNR as a function of voltage level."""

from __future__ import annotations

from typing import Tuple

import numpy as np

from .sensor_class import Sensor
from .sensor_get import sensor_get


def sensor_snr(
    sensor: Sensor, volts: np.ndarray | None = None
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Return the sensor SNR curve.

    Parameters
    ----------
    sensor:
        Sensor object containing noise related attributes such as
        ``conversion_gain`` and ``read_noise_electrons``.  If these are not
        present they default to sensible values (e.g. ``conversion_gain`` of
        ``1.0`` and no additional noise).
    volts:
        Optional voltage levels at which to evaluate the SNR.  When ``None`` a
        logarithmic range from ``1e-4`` to ``sensor.voltage_swing`` is used.

    Returns
    -------
    tuple of arrays
        ``(snr, volts, snr_shot, snr_read, snr_dsnu, snr_prnu)`` where each
        element is a 1-D ``numpy.ndarray``.
    """

    v_swing = sensor_get(sensor, "voltage_swing")
    if volts is None:
        volts = np.logspace(-4, 0, 20) * v_swing
    else:
        volts = np.asarray(volts, dtype=float)

    conv_gain = sensor_get(sensor, "conversion_gain")
    read_sd = sensor_get(sensor, "read_noise_electrons")
    gain_sd = sensor_get(sensor, "gain_sd") / 100.0
    offset_sd = sensor_get(sensor, "offset_sd")

    shot_sd = np.sqrt(volts / conv_gain)
    prnu_sd = gain_sd * (volts / conv_gain)
    dsnu_sd = offset_sd / conv_gain

    signal_power = (volts / conv_gain) ** 2
    noise_power = shot_sd**2 + read_sd**2 + dsnu_sd**2 + prnu_sd**2

    snr = 10.0 * np.log10(signal_power / noise_power)

    snr_shot = 10.0 * np.log10(signal_power / (shot_sd**2))
    snr_read = (
        np.full_like(snr, np.inf)
        if read_sd == 0
        else 10.0 * np.log10(signal_power / (read_sd**2))
    )
    snr_dsnu = (
        np.full_like(snr, np.inf)
        if dsnu_sd == 0
        else 10.0 * np.log10(signal_power / (dsnu_sd**2))
    )
    snr_prnu = (
        np.full_like(snr, np.inf)
        if np.all(prnu_sd == 0)
        else 10.0 * np.log10(signal_power / (prnu_sd**2))
    )

    return snr, volts, snr_shot, snr_read, snr_dsnu, snr_prnu


__all__ = ["sensor_snr"]

