"""Adjust display primaries to achieve a specified white point."""

from __future__ import annotations

import numpy as np

from .display_class import Display
from ..ie_xyz_from_energy import ie_xyz_from_energy
from ..xyy_to_xyz import xyy_to_xyz


def display_set_white_point(display: Display, xy: tuple[float, float] | list[float] | np.ndarray) -> None:
    """Scale ``display.spd`` so that its white point matches ``xy``."""
    spd = np.asarray(display.spd, dtype=float)
    wave = np.asarray(display.wave, dtype=float)

    xy = np.asarray(xy, dtype=float).reshape(2)
    Y = display.max_luminance if display.max_luminance is not None else ie_xyz_from_energy(spd.sum(axis=1), wave).reshape(3)[1]
    target_xyz = xyy_to_xyz(np.array([[xy[0], xy[1], Y]])).reshape(3)

    prim_xyz = ie_xyz_from_energy(spd.T, wave)
    scale = np.linalg.lstsq(prim_xyz, target_xyz, rcond=None)[0]
    display.spd = spd * scale.reshape(1, -1)
    display.white_point = ie_xyz_from_energy(display.spd.sum(axis=1), wave).reshape(3)
    display.max_luminance = display.white_point[1]


__all__ = ["display_set_white_point"]
