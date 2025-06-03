# mypy: ignore-errors
from __future__ import annotations

from typing import Any

from .vcimage_class import VCImage
from ..ie_param_format import ie_param_format


def ip_get(ip: VCImage, param: str) -> Any:
    """Return a parameter value from ``ip``."""
    key = ie_param_format(param)
    if key == "rgb":
        return ip.rgb
    if key == "wave":
        return ip.wave
    if key in {"nwave", "n_wave"}:
        return len(ip.wave)
    if key == "name":
        return getattr(ip, "name", None)
    if key == "demosaicmethod":
        return getattr(ip, "demosaic_method", None)
    if key == "internalcs":
        return getattr(ip, "internal_cs", None)
    if key == "conversionmethodsensor":
        return getattr(ip, "conversion_method_sensor", None)
    if key == "illuminantcorrectionmethod":
        return getattr(ip, "illuminant_correction_method", None)
    raise KeyError(f"Unknown VCImage parameter '{param}'")
