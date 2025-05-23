"""Retrieve parameters from :class:`Scene` objects."""

from __future__ import annotations

from typing import Any

import numpy as np

from .scene_class import Scene
from ..luminance_from_photons import luminance_from_photons


def scene_get(scene: Scene, param: str) -> Any:
    """Return a parameter value from ``scene``.

    Supported parameters are ``photons``, ``wave``, ``n_wave``/``nwave``,
    ``name``, and ``luminance``.
    """
    key = param.lower().replace(" ", "")
    if key == "photons":
        return scene.photons
    if key == "wave":
        return scene.wave
    if key in {"nwave", "n_wave"}:
        return len(scene.wave)
    if key == "name":
        return getattr(scene, "name", None)
    if key == "luminance":
        return luminance_from_photons(scene.photons, scene.wave)
    raise KeyError(f"Unknown scene parameter '{param}'")
