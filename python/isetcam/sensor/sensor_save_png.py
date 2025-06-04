# mypy: ignore-errors
"""Save a Sensor image as a PNG file."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import imageio.v2 as imageio

from .sensor_class import Sensor
from ..display import Display, display_create, display_render
from ..srgb_to_lrgb import srgb_to_lrgb
from ..ie_xyz_from_photons import ie_xyz_from_photons
from ..srgb_xyz import xyz_to_srgb


def sensor_save_png(
    sensor: Sensor, path: str | Path, display: Display | None = None
) -> None:
    """Render ``sensor`` to sRGB and save to ``path``."""
    if display is None:
        display = display_create()

    volts = np.asarray(sensor.volts, dtype=float)
    if volts.ndim != 3 or volts.shape[2] != 3:
        raise ValueError("sensor.volts must be (rows, cols, 3)")

    lrgb = srgb_to_lrgb(volts)
    spectral = display_render(lrgb, display, apply_gamma=True)
    xyz = ie_xyz_from_photons(spectral, display.wave)
    srgb, _, _ = xyz_to_srgb(xyz)

    arr = (np.clip(srgb, 0.0, 1.0) * 255).round().astype(np.uint8)
    imageio.imwrite(str(Path(path)), arr)


__all__ = ["sensor_save_png"]
