# mypy: ignore-errors
"""Assign parameters on :class:`OpticalImage` objects."""

from __future__ import annotations

from typing import Any

import numpy as np

from .oi_class import OpticalImage
from ..ie_param_format import ie_param_format


def oi_set(oi: OpticalImage, param: str, val: Any) -> None:
    """Set a parameter value on ``oi``.

    Supported parameters are ``photons``, ``wave`` and ``name``. ``n_wave`` and
    ``luminance`` are derived values and therefore cannot be set.
    """
    key = ie_param_format(param)
    if key == "photons":
        oi.photons = np.asarray(val)
        return
    if key == "wave":
        oi.wave = np.asarray(val)
        return
    if key == "name":
        oi.name = None if val is None else str(val)
        return
    raise KeyError(f"Unknown or read-only optical image parameter '{param}'")
