# mypy: ignore-errors
from __future__ import annotations

import numpy as np

from .sensor_class import Sensor


def sensor_photon_noise(sensor: Sensor) -> tuple[np.ndarray, np.ndarray]:
    """Apply photon noise to sensor volts.

    A Gaussian approximation is used when the mean signal is at least 15;
    otherwise samples are drawn from a Poisson distribution. The ``sensor``
    object is updated with the noisy volts.

    Parameters
    ----------
    sensor : Sensor
        Sensor providing the mean voltage data.

    Returns
    -------
    tuple of np.ndarray
        ``(noisy_volts, noise)`` where ``noisy_volts`` are the volts with
        noise added and ``noise`` is the difference from the mean volts.
    """
    volts = np.asarray(sensor.volts, dtype=float)

    noisy = np.empty_like(volts, dtype=float)
    noise = np.empty_like(volts, dtype=float)

    mask = volts >= 15
    if np.any(mask):
        g_noise = np.sqrt(volts[mask]) * np.random.randn(*volts[mask].shape)
        noisy[mask] = volts[mask] + g_noise
        noise[mask] = g_noise
    if np.any(~mask):
        samples = np.random.poisson(volts[~mask])
        noisy[~mask] = samples
        noise[~mask] = samples - volts[~mask]

    sensor.volts = noisy
    return noisy, noise
