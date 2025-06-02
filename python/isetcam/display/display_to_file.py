# mypy: ignore-errors
"""Utilities for saving :class:`Display` objects to disk."""

from __future__ import annotations

from pathlib import Path

from scipy.io import savemat

from .display_class import Display


def display_to_file(display: Display, path: str | Path) -> None:
    """Save ``display`` to ``path`` as a MATLAB ``.mat`` file.

    The structure is stored under the variable name ``'d'``.
    """
    data = {
        "spd": display.spd,
        "wave": display.wave,
        "gamma": display.gamma,
    }
    if display.name is not None:
        data["name"] = display.name
    savemat(str(Path(path)), {"d": data})
