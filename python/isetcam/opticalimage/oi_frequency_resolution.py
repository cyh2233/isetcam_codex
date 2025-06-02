"""Frequency resolution for :class:`OpticalImage` objects."""

from __future__ import annotations

import numpy as np

from .oi_class import OpticalImage
from .oi_frequency_support import _unit_frequency_list


def _deg_per_unit(oi: OpticalImage, units: str) -> float:
    """Return degrees per spatial unit for ``oi``."""
    spacing = float(getattr(oi, "sample_spacing", 1.0))
    width_m = oi.photons.shape[1] * spacing
    wangular = getattr(oi, "wangular", None)
    if wangular is None:
        raise ValueError("oi must define 'wangular' field of view")
    deg_per_meter = float(wangular) / width_m
    u = units.lower()
    if u in {"m", "meter", "meters"}:
        return deg_per_meter
    if u in {"mm", "millimeter", "millimeters"}:
        return deg_per_meter * 1e-3
    if u in {"um", "micron", "microns", "micrometer", "micrometers"}:
        return deg_per_meter * 1e-6
    raise ValueError(f"Unknown spatial unit '{units}'")


def oi_frequency_resolution(
    oi: OpticalImage, units: str = "cyclesPerDegree"
) -> dict[str, np.ndarray]:
    """Return frequency resolution of ``oi``.

    Parameters
    ----------
    oi : OpticalImage
        Input optical image.
    units : str, optional
        Output units. Supported values are "cyclesPerDegree"/"cpd",
        "cyclesPerMeter"/"cpm", "cyclesPerMillimeter"/"mm", and
        "cyclesPerMicron"/"um".

    Returns
    -------
    dict
        ``{"fx": fx, "fy": fy}`` arrays giving spatial frequency coordinates.
    """
    spacing = float(getattr(oi, "sample_spacing", 1.0))
    height, width = oi.photons.shape[:2]

    width_m = width * spacing
    height_m = height * spacing

    wangular = getattr(oi, "wangular", None)
    if wangular is None:
        raise ValueError("oi must define 'wangular' field of view")
    wangular = float(wangular)

    dist = width_m / (2.0 * np.tan(np.deg2rad(wangular) / 2.0))
    hangular = np.degrees(2.0 * np.arctan((height_m / 2.0) / dist))

    max_fx_cpd = (width / 2.0) / wangular
    max_fy_cpd = (height / 2.0) / hangular

    u = units.lower()
    if u in {"cyclesperdegree", "cycperdeg", "cpd"}:
        max_fx = max_fx_cpd
        max_fy = max_fy_cpd
    elif u in {"cyclespermeter", "cpm", "m", "meter", "meters"}:
        scale = _deg_per_unit(oi, "m")
        max_fx = max_fx_cpd * scale
        max_fy = max_fy_cpd * scale
    elif u in {"cyclespermillimeter", "mm", "millimeter", "millimeters"}:
        scale = _deg_per_unit(oi, "mm")
        max_fx = max_fx_cpd * scale
        max_fy = max_fy_cpd * scale
    elif u in {
        "cyclespermicron",
        "um",
        "micron",
        "microns",
        "micrometer",
        "micrometers",
    }:
        scale = _deg_per_unit(oi, "um")
        max_fx = max_fx_cpd * scale
        max_fy = max_fy_cpd * scale
    else:
        raise ValueError(f"Unknown frequency unit '{units}'")

    fx = _unit_frequency_list(width) * max_fx
    fy = _unit_frequency_list(height) * max_fy
    return {"fx": fx, "fy": fy}


__all__ = ["oi_frequency_resolution"]
