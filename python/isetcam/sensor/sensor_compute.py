# mypy: ignore-errors
"""Compute sensor response from an optical image."""

from __future__ import annotations

import numpy as np

from ..opticalimage import OpticalImage
from .sensor_class import Sensor
from .sensor_get import sensor_get
from .sensor_add_noise import sensor_add_noise
from .sensor_gain_offset import sensor_gain_offset


def _parse_pattern(letters: np.ndarray | str) -> np.ndarray | None:
    """Return CFA pattern array if ``letters`` encodes a square pattern."""
    if isinstance(letters, str):
        size = int(np.sqrt(len(letters)))
        if size * size == len(letters):
            return np.array(list(letters)).reshape(size, size)
        return None
    letters = np.asarray(letters)
    if letters.ndim == 2:
        return letters
    if letters.ndim == 1:
        size = int(np.sqrt(letters.size))
        if size * size == letters.size:
            return letters.reshape(size, size)
    return None


def auto_exposure(sensor: Sensor, oi: OpticalImage, level: float = 0.95) -> float:
    """Return exposure time that keeps peak signal below ``level`` of swing."""

    if oi.photons.shape[-1] != sensor.wave.size:
        raise ValueError("OpticalImage and Sensor must have matching wavelengths")

    qe = getattr(sensor, "qe", np.ones(sensor.wave.size, dtype=float))
    qe = np.asarray(qe, dtype=float)
    if qe.size != sensor.wave.size:
        raise ValueError("sensor.qe length must match sensor.wave")

    photons = np.asarray(oi.photons, dtype=float) * qe

    if hasattr(sensor, "filter_spectra") and hasattr(sensor, "filter_color_letters"):
        fs = np.asarray(sensor.filter_spectra, dtype=float)
        if fs.shape[0] != sensor.wave.size:
            raise ValueError("filter_spectra first dimension must match sensor.wave")
        pattern = _parse_pattern(getattr(sensor, "filter_color_letters"))
        if pattern is None:
            raise ValueError("filter_color_letters must form a square CFA pattern")
        fnames = getattr(sensor, "filter_names", None)
        if fnames is None:
            raise AttributeError("sensor missing 'filter_names'")
        letter_map = {str(n)[0].lower(): i for i, n in enumerate(fnames)}
        pr, pc = pattern.shape
        rows, cols = sensor.volts.shape[:2]
        mosaic = np.tile(pattern, (rows // pr + 1, cols // pc + 1))[:rows, :cols]
        max_signal = 0.0
        for letter in np.unique(mosaic):
            idx = letter_map.get(str(letter).lower())
            if idx is None:
                raise ValueError(f"Unknown CFA letter '{letter}'")
            spectral = fs[:, idx]
            integ = (photons * spectral).sum(axis=2)
            val = float(np.max(integ[mosaic == letter]))
            if val > max_signal:
                max_signal = val
    else:
        max_signal = float((photons.sum(axis=2)).max())

    if max_signal <= 0:
        return 0.0

    v_swing = sensor_get(sensor, "voltage_swing")
    return float(level * v_swing / max_signal)


def sensor_compute(sensor: Sensor, oi: OpticalImage) -> Sensor:
    """Integrate photons in ``oi`` to produce sensor volts.

    Parameters
    ----------
    sensor : Sensor
        Sensor dataclass which may optionally contain a ``qe`` attribute
        giving the quantum efficiency for each wavelength sample.
    oi : OpticalImage
        Optical image providing photon data.

    Returns
    -------
    Sensor
        ``sensor`` with its ``volts`` attribute set to the integrated
        response.
    """
    if oi.photons.shape[-1] != sensor.wave.size:
        raise ValueError("OpticalImage and Sensor must have matching wavelengths")

    if getattr(sensor, "auto_exposure", False):
        sensor.exposure_time = auto_exposure(sensor, oi)

    qe = getattr(sensor, "qe", np.ones(sensor.wave.size, dtype=float))
    qe = np.asarray(qe, dtype=float)
    if qe.size != sensor.wave.size:
        raise ValueError("sensor.qe length must match sensor.wave")

    photons = np.asarray(oi.photons, dtype=float) * qe

    if hasattr(sensor, "filter_spectra") and hasattr(sensor, "filter_color_letters"):
        fs = np.asarray(sensor.filter_spectra, dtype=float)
        if fs.shape[0] != sensor.wave.size:
            raise ValueError("filter_spectra first dimension must match sensor.wave")
        pattern = _parse_pattern(getattr(sensor, "filter_color_letters"))
        if pattern is None:
            raise ValueError("filter_color_letters must form a square CFA pattern")
        fnames = getattr(sensor, "filter_names", None)
        if fnames is None:
            raise AttributeError("sensor missing 'filter_names'")
        letter_map = {str(n)[0].lower(): i for i, n in enumerate(fnames)}
        pr, pc = pattern.shape
        rows, cols = sensor.volts.shape[:2]
        mosaic = np.tile(pattern, (rows // pr + 1, cols // pc + 1))[:rows, :cols]
        volts = np.zeros((rows, cols), dtype=float)
        for letter in np.unique(mosaic):
            idx = letter_map.get(str(letter).lower())
            if idx is None:
                raise ValueError(f"Unknown CFA letter '{letter}'")
            spectral = fs[:, idx]
            integ = (photons * spectral).sum(axis=2) * float(sensor.exposure_time)
            volts[mosaic == letter] = integ[mosaic == letter]
    else:
        volts = photons.sum(axis=2) * float(sensor.exposure_time)

    sensor.volts = volts

    sensor_add_noise(sensor)
    gain = getattr(sensor, "analog_gain", 1.0)
    offset = getattr(sensor, "analog_offset", 0.0)
    sensor_gain_offset(sensor, gain=gain, offset=offset)

    return sensor

