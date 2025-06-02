# mypy: ignore-errors
"""Generate a grid line pattern scene."""

from __future__ import annotations

import numpy as np

from .scene_class import Scene
from ..illuminant import illuminant_create
from ..energy_to_quanta import energy_to_quanta

_DEF_WAVE = np.arange(400, 701, 10, dtype=float)


def scene_grid_lines(
    size: int = 128,
    spacing: int = 16,
    spectral_type: str = "d65",
    line_thickness: int = 1,
) -> Scene:
    """Return a grid line scene for resolution testing.

    Parameters
    ----------
    size : int, optional
        Height and width of the square scene in pixels. Defaults to ``128``.
    spacing : int, optional
        Number of pixels between grid lines. Defaults to ``16``.
    spectral_type : {"d65", "ee", "ep"}, optional
        Spectrum of the lines. ``"d65"`` uses the D65 illuminant,
        ``"ee"`` equal energy, and ``"ep"`` equal photons. Defaults to ``"d65"``.
    line_thickness : int, optional
        Width of the lines in pixels. Defaults to ``1``.

    Returns
    -------
    Scene
        Generated scene containing the grid pattern and default wavelength
        sampling.
    """

    wave = _DEF_WAVE

    stype = spectral_type.lower()
    if stype == "d65":
        ill = illuminant_create("D65", wave)
        ill_photons = ill.spd.astype(float)
    elif stype in {"ee", "equalenergy"}:
        ill_photons = energy_to_quanta(wave, np.ones_like(wave)).ravel()
    elif stype in {"ep", "equalphoton", "equalphotons"}:
        ill_photons = np.ones_like(wave, dtype=float)
    else:
        raise ValueError(f"Unknown spectral_type '{spectral_type}'")

    pattern = np.full((size, size), 1e-5, dtype=float)
    half = spacing // 2
    for t in range(line_thickness):
        rows = np.arange(half + t, size, spacing)
        cols = np.arange(half + t, size, spacing)
        pattern[rows, :] = 1.0
        pattern[:, cols] = 1.0

    photons = pattern[:, :, None] * ill_photons[None, None, :]

    sc = Scene(photons=photons, wave=wave, name="Grid lines")
    sc.illuminant = ill_photons
    return sc


__all__ = ["scene_grid_lines"]
