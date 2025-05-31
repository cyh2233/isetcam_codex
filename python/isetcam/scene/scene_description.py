"""Generate a short textual description of a :class:`Scene`."""

from __future__ import annotations

import numpy as np

from .scene_class import Scene
from .scene_get import scene_get
from ..luminance_from_photons import luminance_from_photons


ndefault = "No scene structure"


def scene_description(scene: Scene | None) -> str:
    """Return a multi-line description of ``scene``."""
    if scene is None:
        return ndefault

    lines: list[str] = []
    name = scene_get(scene, "name")
    if name:
        lines.append(f"Name:\t{name}")

    photons = np.asarray(scene_get(scene, "photons"))
    if photons.size:
        rows, cols = photons.shape[:2]
        lines.append(f"Size:\t{rows} x {cols}")

    wave = np.asarray(scene_get(scene, "wave"), dtype=float)
    if wave.size:
        spacing = wave[1] - wave[0] if wave.size > 1 else 0
        lines.append(f"Wave:\t{int(wave[0])}:{int(spacing)}:{int(wave[-1])} nm")

    lum = luminance_from_photons(photons, wave)
    if lum.size:
        lines.append(f"Mean luminance:\t{float(lum.mean()):.4g} cd/m^2")

    return "\n".join(lines) if lines else ndefault


__all__ = ["scene_description"]
