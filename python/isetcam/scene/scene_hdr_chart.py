"""Create an HDR chart with luminance steps."""

from __future__ import annotations

from typing import Optional

import numpy as np

from .scene_class import Scene
from .scene_adjust_luminance import scene_adjust_luminance
from ..illuminant import illuminant_create

_DEF_WAVE = np.arange(400, 701, 10, dtype=float)


def scene_hdr_chart(
    dynamic_range: float = 1e4,
    n_levels: int = 12,
    cols_per_level: int = 8,
    *,
    max_luminance: Optional[float] = None,
    wave: np.ndarray | None = None,
) -> Scene:
    """Return a chart of horizontal strips spanning ``dynamic_range``."""

    if wave is None:
        wave = _DEF_WAVE
    else:
        wave = np.asarray(wave, dtype=float).reshape(-1)

    ill = illuminant_create("D65", wave)
    ill_photons = ill.spd.astype(float)

    cols = n_levels * cols_per_level
    rows = cols

    reflectances = np.logspace(0, np.log10(1.0 / dynamic_range), n_levels)
    photons = ill_photons[:, None] * reflectances

    img = np.zeros((rows, cols, wave.size), dtype=float)
    for i in range(n_levels):
        start = i * cols_per_level
        end = start + cols_per_level
        patch = photons[:, i]
        img[:, start:end, :] = patch

    sc = Scene(photons=img, wave=wave, name="HDR chart")
    if max_luminance is not None:
        sc = scene_adjust_luminance(sc, "peak", float(max_luminance))
    return sc
