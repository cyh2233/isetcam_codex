# mypy: ignore-errors
"""Convert a hyperspectral cube to sRGB for display."""

from __future__ import annotations

import numpy as np

from ..ie_xyz_from_photons import ie_xyz_from_photons
from ..srgb_xyz import xyz_to_srgb


def hc_image(cube: np.ndarray, wave: np.ndarray) -> np.ndarray:
    """Return an sRGB image of ``cube`` sampled at ``wave``."""
    cube = np.asarray(cube, dtype=float)
    if cube.ndim != 3:
        raise ValueError("cube must be 3-D")

    xyz = ie_xyz_from_photons(cube, wave)
    srgb, _, _ = xyz_to_srgb(xyz)
    return np.clip(srgb, 0.0, 1.0)

