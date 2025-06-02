# mypy: ignore-errors
"""Retrieve parameters from :class:`OpticalImage` objects."""

from __future__ import annotations

from typing import Any

import numpy as np

from .oi_class import OpticalImage
from ..luminance_from_photons import luminance_from_photons
from ..ie_param_format import ie_param_format


def oi_get(oi: OpticalImage, param: str) -> Any:
    """Return a parameter value from ``oi``.

    Supported parameters are ``photons``, ``wave``, ``n_wave``/``nwave``,
    ``name``, and ``luminance``.
    """
    key = ie_param_format(param)
    if key == "photons":
        return oi.photons
    if key == "wave":
        return oi.wave
    if key in {"nwave", "n_wave"}:
        return len(oi.wave)
    if key == "name":
        return getattr(oi, "name", None)
    if key == "luminance":
        return luminance_from_photons(oi.photons, oi.wave)
    raise KeyError(f"Unknown optical image parameter '{param}'")
