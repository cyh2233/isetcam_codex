# mypy: ignore-errors
from __future__ import annotations

import numpy as np

from ..illuminant import illuminant_create
from ..energy_to_quanta import energy_to_quanta
from ..opticalimage import OpticalImage, oi_calculate_illuminance
from ..sensor.sensor_compute import sensor_compute
from ..sensor.sensor_get import sensor_get
from ..sensor.sensor_class import Sensor


def _uniform_d65_oi(wave: np.ndarray) -> OpticalImage:
    ill = illuminant_create("D65", wave)
    photons = energy_to_quanta(ill.wave, ill.spd)
    photons = photons.reshape(1, 1, -1)
    return OpticalImage(photons=photons, wave=wave, name="Uniform D65")


def iso_speed_saturation(sensor: Sensor) -> float:
    """Return ISO saturation speed for ``sensor`` using a D65 source."""
    well_capacity = getattr(sensor, "well_capacity", None)
    if well_capacity is None:
        raise AttributeError("sensor must have 'well_capacity' attribute")

    wave = sensor.wave
    oi = _uniform_d65_oi(wave)

    tmp = sensor_compute(sensor, oi)
    electrons = float(np.mean(tmp.volts))

    lux = float(oi_calculate_illuminance(oi).mean())
    lux_sec = lux * sensor_get(sensor, "exposure_time")

    sat_lux_sec = lux_sec * (well_capacity / electrons)

    return 10.0 / ((sat_lux_sec / np.sqrt(2.0)) * 0.14)


__all__ = ["iso_speed_saturation"]
