# mypy: ignore-errors
"""Create a checkerboard test scene."""

from __future__ import annotations

import numpy as np

from .scene_class import Scene
from ..illuminant import illuminant_create

_DEF_WAVE = np.arange(400, 701, 10, dtype=float)


def _illuminant_photons(wave: np.ndarray, spectral_type: str) -> np.ndarray:
    stype = spectral_type.lower().replace(" ", "")
    if stype == "d65":
        ill = illuminant_create("D65", wave)
        return ill.spd.astype(float)
    if stype in {"ee", "equalenergy"}:
        return np.ones_like(wave, dtype=float)
    if stype in {"ep", "equalphoton", "equalphotons"}:
        return np.ones_like(wave, dtype=float)
    raise ValueError(f"Unknown spectral_type '{spectral_type}'")


def scene_checkerboard(
    pixels_per_check: int,
    n_checks: int,
    spectral_type: str = "d65",
) -> Scene:
    """Return a checkerboard pattern scene.

    Parameters
    ----------
    pixels_per_check : int
        Size of each square in pixels.
    n_checks : int
        Number of black/white check pairs along each axis.
    spectral_type : {'d65', 'ee', 'equalenergy', 'ep', 'equalphotons'}, optional
        Type of illuminant used for the checkerboard. Defaults to ``'d65'``.

    Returns
    -------
    Scene
        Checkerboard scene with photon data scaled by the chosen illuminant.
    """

    pp = int(pixels_per_check)
    nc = int(n_checks)
    if pp <= 0 or nc <= 0:
        raise ValueError("pixels_per_check and n_checks must be > 0")

    base = np.kron([[0, 1], [1, 0]], np.ones((pp, pp), dtype=float))
    pattern = np.tile(base, (nc, nc))
    pattern = pattern / pattern.max()
    pattern = np.clip(pattern, 1e-6, 1.0)

    wave = _DEF_WAVE
    ill_photons = _illuminant_photons(wave, spectral_type)
    img = pattern[:, :, None] * ill_photons[None, None, :]
    name = f"Checker-{spectral_type}"
    return Scene(photons=img, wave=wave, name=name)


__all__ = ["scene_checkerboard"]
