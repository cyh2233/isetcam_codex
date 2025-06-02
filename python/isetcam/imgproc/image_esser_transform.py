# mypy: ignore-errors
"""Calculate sensor-to-target transform using the Esser chart."""

from __future__ import annotations

from pathlib import Path
from typing import Sequence

import numpy as np

from ..ie_read_spectra import ie_read_spectra
from ..illuminant import illuminant_create
from ..energy_to_quanta import energy_to_quanta
from ..data_path import data_path


def image_esser_transform(
    sensor_qe: np.ndarray,
    target_qe: np.ndarray,
    wave: Sequence[float],
    illuminant: str | Sequence[float] = "D65",
    *,
    surfaces: np.ndarray | None = None,
) -> np.ndarray:
    """Return linear transform from sensor space to target space."""
    sensor_qe = np.asarray(sensor_qe, dtype=float)
    target_qe = np.asarray(target_qe, dtype=float)
    wave = np.asarray(wave, dtype=float)

    if sensor_qe.shape[0] != wave.size or target_qe.shape[0] != wave.size:
        raise ValueError("sensor_qe and target_qe must match wave length")

    if surfaces is None:
        path = data_path("surfaces/charts/esser/reflectance/esserChart.mat")
        surfaces, _, _, _ = ie_read_spectra(path, wave)
    else:
        surfaces = np.asarray(surfaces, dtype=float)
        if surfaces.shape[0] != wave.size:
            raise ValueError("surfaces rows must match wave length")

    if isinstance(illuminant, str):
        illum = illuminant_create(illuminant, wave)
        ill_energy = illum.spd
    else:
        ill_energy = np.asarray(illuminant, dtype=float)
        if ill_energy.size != wave.size:
            raise ValueError("Illuminant length must match wave")

    ill_quanta = energy_to_quanta(wave, ill_energy).reshape(-1)

    sensor_esser = (sensor_qe.T @ np.diag(ill_quanta) @ surfaces).T
    target_esser = (target_qe.T @ np.diag(ill_quanta) @ surfaces).T

    T, _, _, _ = np.linalg.lstsq(sensor_esser, target_esser, rcond=None)
    return T

__all__ = ["image_esser_transform"]
