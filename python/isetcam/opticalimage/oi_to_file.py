# mypy: ignore-errors
"""Utilities for saving :class:`OpticalImage` objects to disk."""

from __future__ import annotations

from pathlib import Path

from scipy.io import savemat

from .oi_class import OpticalImage


def oi_to_file(oi: OpticalImage, path: str | Path) -> None:
    """Save ``oi`` to ``path`` as a MATLAB ``.mat`` file.

    Only the ``photons`` and ``wave`` fields are stored under the variable
    name ``'oi'``.
    """
    data = {"photons": oi.photons, "wave": oi.wave}
    if oi.name is not None:
        data["name"] = oi.name
    savemat(str(Path(path)), {"oi": data})
