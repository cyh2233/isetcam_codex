from __future__ import annotations

import numpy as np

from .sensor_class import Sensor
from .sensor_get import sensor_get


def sensor_add_noise(sensor: Sensor) -> tuple[np.ndarray, np.ndarray]:
    """Add DSNU and PRNU noise to ``sensor.volts``.

    The function draws additive dark-signal non-uniformity (DSNU) noise
    from a Gaussian distribution with standard deviation given by
    ``sensor_get(sensor, "offset_sd")`` and multiplicative pixel response
    non-uniformity (PRNU) noise with standard deviation
    ``sensor_get(sensor, "gain_sd")`` percent around unity.  The ``sensor``
    object is updated with the noisy volts.

    Parameters
    ----------
    sensor : Sensor
        Sensor containing voltage data and optional noise parameters.

    Returns
    -------
    tuple of np.ndarray
        ``(noisy_volts, noise)`` where ``noisy_volts`` are the volts with
        noise added and ``noise`` is the difference from the original volts.
    """
    volts = np.asarray(sensor.volts, dtype=float)

    gain_sd = sensor_get(sensor, "gain_sd") / 100.0
    offset_sd = sensor_get(sensor, "offset_sd")

    if gain_sd == 0:
        gain = 1.0
    else:
        gain = 1.0 + gain_sd * np.random.randn(*volts.shape)

    if offset_sd == 0:
        offset = 0.0
    else:
        offset = offset_sd * np.random.randn(*volts.shape)

    noisy = volts * gain + offset
    sensor.volts = noisy
    noise = noisy - volts
    return noisy, noise
