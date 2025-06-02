# mypy: ignore-errors
"""Scale illuminant so mean cube reflectance is unity."""

from __future__ import annotations

import numpy as np


def _expand_illuminant(illuminant: np.ndarray, shape: tuple[int, int, int]) -> np.ndarray:
    """Return ``illuminant`` expanded to ``shape``."""
    illuminant = np.asarray(illuminant, dtype=float)
    if illuminant.ndim == 1:
        if illuminant.size != shape[2]:
            raise ValueError("Illuminant vector length must match cube bands")
        return np.tile(illuminant.reshape(1, 1, -1), (shape[0], shape[1], 1))
    if illuminant.ndim == 3:
        if illuminant.shape != shape:
            raise ValueError("Illuminant cube must match data shape")
        return illuminant
    raise ValueError("Illuminant must be 1-D or 3-D")


def hc_illuminant_scale(cube: np.ndarray, illuminant: np.ndarray) -> np.ndarray:
    """Return scaled illuminant with mean cube reflectance equal to one."""
    cube = np.asarray(cube, dtype=float)
    ill_cube = _expand_illuminant(illuminant, cube.shape)
    with np.errstate(divide='ignore', invalid='ignore'):
        refl = np.divide(cube, ill_cube, out=np.zeros_like(cube), where=ill_cube!=0)
    avg_refl = float(refl.mean())
    scale = avg_refl if avg_refl > 0 else 1.0
    return illuminant * scale

