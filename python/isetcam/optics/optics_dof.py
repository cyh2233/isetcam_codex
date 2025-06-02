# mypy: ignore-errors
"""Compute depth of field for a thin lens."""

from __future__ import annotations

from .optics_class import Optics
from .optics_get import optics_get


def optics_dof(optics: Optics, o_dist: float, coc_diam: float = 10e-6) -> float:
    """Return depth of field in meters.

    Parameters
    ----------
    optics : Optics
        Lens description.
    o_dist : float
        Object distance from lens in meters.
    coc_diam : float, optional
        Acceptable circle of confusion diameter in meters. Default ``10e-6``.

    Returns
    -------
    float
        Depth of field corresponding to ``o_dist``.
    """
    if optics is None:
        raise ValueError("optics is required")

    f_num = optics_get(optics, "fnumber")
    f_len = optics_get(optics, "focal length")
    return 2.0 * f_num * coc_diam * (o_dist ** 2) / (f_len ** 2)
