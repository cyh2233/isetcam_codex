"""Assign parameters on :class:`Scene` objects."""

from __future__ import annotations

from typing import Any

import numpy as np

from .scene_class import Scene


def scene_set(scene: Scene, param: str, val: Any) -> None:
    """Set a parameter value on ``scene``.

    Supported parameters are ``photons``, ``wave`` and ``name``. ``n_wave`` and
    ``luminance`` are derived values and therefore cannot be set.
    """
    key = param.lower().replace(" ", "")
    if key == "photons":
        scene.photons = np.asarray(val)
        return
    if key == "wave":
        scene.wave = np.asarray(val)
        return
    if key == "name":
        scene.name = None if val is None else str(val)
        return
    raise KeyError(f"Unknown or read-only scene parameter '{param}'")
