"""Frequency support for :class:`OpticalImage` objects."""

from __future__ import annotations

import numpy as np

from .oi_class import OpticalImage


def _unit_frequency_list(n: int) -> np.ndarray:
    idx = np.arange(n)
    mid = n // 2
    if n % 2:
        mid = (n - 1) // 2
    c = idx - mid
    if c.max() == 0:
        return c.astype(float)
    return c / np.max(np.abs(c))


def _freq_scale(units: str) -> float:
    units = units.lower()
    if units in {"cyclesperdegree", "cycperdeg", "cpd"}:
        return 1.0
    if units in {"cyclespermeter", "cpm", "m", "meter", "meters"}:
        return 1.0
    if units in {"cyclespermillimeter", "mm", "millimeter", "millimeters"}:
        return 1e-3
    if units in {"cyclespermicron", "um", "micron", "microns", "micrometer", "micrometers"}:
        return 1e-6
    raise ValueError(f"Unknown frequency unit '{units}'")


def oi_frequency_support(oi: OpticalImage, units: str = "cyclesPerDegree") -> dict[str, np.ndarray]:
    """Return frequency support of ``oi``.

    Parameters
    ----------
    oi : OpticalImage
        Input optical image.
    units : str, optional
        Output units. Defaults to ``"cyclesPerDegree"``.

    Returns
    -------
    dict
        ``{"fx": fx, "fy": fy}`` arrays giving spatial frequency coordinates.
    """
    spacing = getattr(oi, "sample_spacing", 1.0)
    height, width = oi.photons.shape[:2]

    nyquist_x = 1.0 / (2 * spacing)
    nyquist_y = 1.0 / (2 * spacing)

    fx = _unit_frequency_list(width) * nyquist_x
    fy = _unit_frequency_list(height) * nyquist_y

    scale = _freq_scale(units)
    return {"fx": fx / scale, "fy": fy / scale}
