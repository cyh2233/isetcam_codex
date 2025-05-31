from __future__ import annotations

from typing import Sequence, Tuple

import numpy as np

from .sensor_class import Sensor
from .sensor_photon_noise import sensor_photon_noise


def sensor_stats(
    sensor: Sensor,
    roi: Sequence[int],
    *,
    use_photon_noise: bool = False,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return mean signal, noise SD and SNR for a sensor ROI.

    Parameters
    ----------
    sensor : Sensor
        Sensor object containing voltage data.
    roi : sequence of int
        ROI specified as ``(x, y, width, height)`` using 0-based indexing.
    use_photon_noise : bool, optional
        When ``True`` photon noise is generated using
        :func:`sensor_photon_noise` before computing the statistics.  The
        ``sensor`` object is updated with the noisy volts and noise is
        measured from the added noise.  When ``False`` noise is estimated
        from the standard deviation of the ROI data.

    Returns
    -------
    tuple of np.ndarray
        ``(mean_signal, noise_sd, snr)`` for each color channel present in
        ``sensor.volts``.
    """

    if len(roi) != 4:
        raise ValueError("roi must be (x, y, width, height)")
    x, y, w, h = [int(v) for v in roi]
    if w <= 0 or h <= 0:
        raise ValueError("width and height must be positive")

    volts = np.asarray(sensor.volts, dtype=float)
    if x < 0 or y < 0 or x + w > volts.shape[1] or y + h > volts.shape[0]:
        raise ValueError("roi is outside the sensor bounds")

    if use_photon_noise:
        noisy_volts, noise_full = sensor_photon_noise(sensor)
        roi_volts = noisy_volts[y : y + h, x : x + w, ...]
        roi_noise = noise_full[y : y + h, x : x + w, ...]
    else:
        roi_volts = volts[y : y + h, x : x + w, ...]
        roi_noise = roi_volts - np.nanmean(roi_volts, axis=(0, 1), keepdims=True)

    if roi_volts.ndim == 2:
        roi_volts = roi_volts[..., np.newaxis]
        roi_noise = roi_noise[..., np.newaxis]

    flat_volts = roi_volts.reshape(-1, roi_volts.shape[2])
    flat_noise = roi_noise.reshape(-1, roi_noise.shape[2])

    mean_signal = np.nanmean(flat_volts, axis=0)
    noise_sd = np.nanstd(flat_noise, axis=0)
    with np.errstate(divide="ignore", invalid="ignore"):
        snr = np.where(noise_sd == 0, np.inf, mean_signal / noise_sd)
    return mean_signal, noise_sd, snr


__all__ = ["sensor_stats"]
