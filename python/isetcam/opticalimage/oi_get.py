# mypy: ignore-errors
"""Retrieve parameters from :class:`OpticalImage` objects."""

from __future__ import annotations

from typing import Any

import numpy as np

from .oi_class import OpticalImage
from ..luminance_from_photons import luminance_from_photons
from ..ie_param_format import ie_param_format


def oi_get(oi: OpticalImage, param: str, units: str | None = None) -> Any:
    """Return a parameter value from ``oi``.

    Supported parameters include ``photons``, ``wave``, ``n_wave``/``nwave``,
    ``name``, ``luminance``, and several optics parameters.
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
    if key in {"opticsfnumber", "opticsf_number"}:
        if oi.optics_f_number is None:
            return None
        return float(oi.optics_f_number)
    if key in {"opticsfocallength", "opticsf_length"}:
        if oi.optics_f_length is None:
            return None
        val = float(oi.optics_f_length)
        if units == "mm":
            val *= 1e3
        return val
    if key == "opticsaperturediameter":
        if oi.optics_f_number is None or oi.optics_f_length is None:
            return None
        dia = float(oi.optics_f_length) / float(oi.optics_f_number)
        if units == "mm":
            dia *= 1e3
        return dia
    if key == "opticsdiopters":
        if oi.optics_f_length is None:
            return None
        return 1.0 / float(oi.optics_f_length)
    if key == "opticsmodel":
        return oi.optics_model
    raise KeyError(f"Unknown optical image parameter '{param}'")
