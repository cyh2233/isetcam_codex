# mypy: ignore-errors
"""Scale a display's primaries to match a target peak luminance."""

from __future__ import annotations

import numpy as np

from .display_class import Display
from ..ie_xyz_from_energy import ie_xyz_from_energy


def display_set_max_luminance(display: Display, lum: float) -> None:
    """Scale ``display.spd`` so that white luminance equals ``lum`` cd/m^2."""
    spd = np.asarray(display.spd, dtype=float)
    wave = np.asarray(display.wave, dtype=float)
    white_spd = spd.sum(axis=1)
    xyz = ie_xyz_from_energy(white_spd, wave).reshape(3)
    curr_l = xyz[1]
    if curr_l == 0:
        raise ValueError("Display has zero luminance")
    scale = float(lum) / curr_l
    display.spd = spd * scale
    display.max_luminance = float(lum)
    display.white_point = ie_xyz_from_energy(display.spd.sum(axis=1), wave).reshape(3)


__all__ = ["display_set_max_luminance"]
