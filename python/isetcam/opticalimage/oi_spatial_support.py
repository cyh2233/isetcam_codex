"""Spatial support for :class:`OpticalImage` objects."""

from __future__ import annotations

import numpy as np

from .oi_class import OpticalImage


def _unit_scale(units: str) -> float:
    units = units.lower()
    if units in {"m", "meter", "meters"}:
        return 1.0
    if units in {"mm", "millimeter", "millimeters"}:
        return 1e3
    if units in {"um", "micron", "microns", "micrometer", "micrometers"}:
        return 1e6
    raise ValueError(f"Unknown spatial unit '{units}'")


def oi_spatial_support(oi: OpticalImage, units: str = "meters") -> dict[str, np.ndarray]:
    """Return spatial support of ``oi``.

    Parameters
    ----------
    oi : OpticalImage
        Input optical image.
    units : str, optional
        Output units. Supported values are "meters"/"m", "millimeters"/"mm",
        and "microns"/"um".

    Returns
    -------
    dict
        ``{"x": x, "y": y}`` arrays giving sample locations.
    """
    spacing = getattr(oi, "sample_spacing", 1.0)
    height, width = oi.photons.shape[:2]
    x = (np.arange(width) - (width - 1) / 2) * spacing
    y = (np.arange(height) - (height - 1) / 2) * spacing
    scale = _unit_scale(units)
    return {"x": x * scale, "y": y * scale}

