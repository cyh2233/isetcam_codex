# mypy: ignore-errors
"""Resample sensor spectral data to a new wavelength support."""

from __future__ import annotations

from typing import Sequence

import numpy as np

from .sensor_class import Sensor


def _interp_matrix(data: np.ndarray, src_wave: np.ndarray, tgt_wave: np.ndarray) -> np.ndarray:
    """Helper to interpolate columns of ``data`` to ``tgt_wave``."""
    out = np.empty((tgt_wave.size, data.shape[1]), dtype=float)
    for i in range(data.shape[1]):
        out[:, i] = np.interp(tgt_wave, src_wave, data[:, i], left=0.0, right=0.0)
    return out


def sensor_resample_wave(sensor: Sensor, wave: Sequence[float]) -> Sensor:
    """Return ``sensor`` resampled to ``wave``.

    The voltage data are left unchanged but spectral properties such as quantum
    efficiency and color filter spectra are interpolated to the desired
    wavelengths.
    """
    src_wave = np.asarray(sensor.wave, dtype=float).reshape(-1)
    tgt_wave = np.asarray(wave, dtype=float).reshape(-1)

    out = Sensor(
        volts=np.asarray(sensor.volts),
        wave=tgt_wave,
        exposure_time=sensor.exposure_time,
        name=sensor.name,
    )

    qe = getattr(sensor, "qe", None)
    if qe is not None:
        qe = np.asarray(qe, dtype=float).reshape(-1)
        if qe.size != src_wave.size:
            raise ValueError("sensor.qe length must match sensor.wave")
        out.qe = np.interp(tgt_wave, src_wave, qe, left=0.0, right=0.0)

    if hasattr(sensor, "filter_spectra"):
        filt = np.asarray(sensor.filter_spectra, dtype=float)
        if filt.shape[0] != src_wave.size:
            raise ValueError("filter_spectra first dimension must match sensor.wave")
        out.filter_spectra = _interp_matrix(filt, src_wave, tgt_wave)

    if hasattr(sensor, "ir_filter"):
        ir = np.asarray(sensor.ir_filter, dtype=float).reshape(-1)
        if ir.size != src_wave.size:
            raise ValueError("ir_filter length must match sensor.wave")
        out.ir_filter = np.interp(tgt_wave, src_wave, ir, left=0.0, right=0.0)

    return out


__all__ = ["sensor_resample_wave"]
