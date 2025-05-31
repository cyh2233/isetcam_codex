"""Assign parameters on :class:`Illuminant` objects."""

from __future__ import annotations

from typing import Any

import numpy as np

from .illuminant_class import Illuminant
from ..ie_param_format import ie_param_format


def illuminant_set(illuminant: Illuminant, param: str, val: Any) -> None:
    """Set a parameter value on ``illuminant``.

    Supported parameters are ``spd``, ``wave`` and ``name``. ``n_wave`` is
    derived from ``wave`` and therefore cannot be set.
    """
    key = ie_param_format(param)
    if key == "spd":
        illuminant.spd = np.asarray(val)
        return
    if key == "wave":
        illuminant.wave = np.asarray(val)
        return
    if key == "name":
        illuminant.name = None if val is None else str(val)
        return
    raise KeyError(f"Unknown or read-only illuminant parameter '{param}'")
