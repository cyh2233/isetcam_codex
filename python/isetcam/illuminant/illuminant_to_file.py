# mypy: ignore-errors
"""Utilities for saving :class:`Illuminant` objects to disk."""

from __future__ import annotations

from pathlib import Path

from scipy.io import savemat

from .illuminant_class import Illuminant


def illuminant_to_file(illuminant: Illuminant, path: str | Path) -> None:
    """Save ``illuminant`` to ``path`` as a MATLAB ``.mat`` file.

    The spectral distribution is stored using the variables ``spd`` and
    ``wavelength``.  When present, the ``name`` field is also saved.
    """
    data = {
        "spd": illuminant.spd,
        "wavelength": illuminant.wave,
    }
    if illuminant.name is not None:
        data["name"] = illuminant.name
    savemat(str(Path(path)), data)
