from __future__ import annotations

from typing import Any

import numpy as np

from .vcimage_class import VCImage
from ..ie_param_format import ie_param_format


def ip_set(ip: VCImage, param: str, val: Any) -> None:
    """Set a parameter value on ``ip``."""
    key = ie_param_format(param)
    if key == "rgb":
        ip.rgb = np.asarray(val)
        return
    if key == "wave":
        ip.wave = np.asarray(val)
        return
    if key == "name":
        ip.name = None if val is None else str(val)
        return
    raise KeyError(f"Unknown or read-only VCImage parameter '{param}'")

