# mypy: ignore-errors
"""Compute circle of confusion diameter."""

from __future__ import annotations

import numpy as np

from .optics_class import Optics


def _unit_scale_factor(unit: str) -> float:
    """Return scale factor to convert meters to ``unit``."""
    u = unit.lower()
    if u in {"m", "meter", "meters"}:
        return 1.0
    if u in {"mm", "millimeter", "millimeters"}:
        return 1e3
    if u in {"um", "micron", "microns", "micrometer", "micrometers"}:
        return 1e6
    if u in {"nm", "nanometer", "nanometers"}:
        return 1e9
    if u in {"cm", "centimeter", "centimeters"}:
        return 1e2
    if u in {"km", "kilometer", "kilometers"}:
        return 1e-3
    if u in {"inches", "inch"}:
        return 39.37007874
    if u in {"foot", "feet"}:
        return 3.280839895
    raise ValueError(f"Unknown unit '{unit}'")


def optics_coc(
    optics: Optics,
    focus_distance: float,
    eval_distance: np.ndarray | float,
    units: str = "m",
) -> np.ndarray:
    """Circle of confusion diameter.

    Parameters
    ----------
    optics : Optics
        Lens description.
    focus_distance : float
        Distance from the lens to the object in perfect focus (meters).
    eval_distance : array-like or float
        Distances from the lens for which to evaluate the circle
        of confusion (meters).
    units : str, optional
        Desired output units. Default is meters.

    Returns
    -------
    np.ndarray
        Circle of confusion diameter for each ``eval_distance``.
    """
    eval_distance = np.asarray(eval_distance, dtype=float).reshape(-1)

    A = optics.f_length / optics.f_number

    fO = 1.0 / ((1.0 / optics.f_length) - (1.0 / focus_distance))

    fX = 1.0 / ((1.0 / optics.f_length) - (1.0 / eval_distance))
    fX = np.maximum(fX, 0.0)

    circ = A * np.abs(fX - fO) / fX

    return circ * _unit_scale_factor(units)
