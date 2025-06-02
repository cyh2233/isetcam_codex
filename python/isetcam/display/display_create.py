# mypy: ignore-errors
"""Factory function for :class:`Display` objects."""

from __future__ import annotations

from pathlib import Path

import numpy as np
from scipy.io import loadmat

from ..data_path import data_path

from .display_class import Display

_DEFAULT_NAME = "LCD-Apple"
_DEF_DIR = "data"


def _load_display(path: Path) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return ``wave``, ``spd`` and ``gamma`` arrays from ``path``."""
    data = loadmat(path)
    if "d" not in data:
        raise KeyError("No display struct 'd' found in file")
    d = data["d"][0, 0]
    wave = d["wave"].ravel().astype(float)
    spd = d["spd"].astype(float)
    gamma = d["gamma"].astype(float)
    return wave, spd, gamma


def display_create(name: str | None = None) -> Display:
    """Create a :class:`Display` by name.

    Parameters
    ----------
    name:
        Name of the display calibration file (without extension). When
        ``None``, the default display is returned.
    """
    if name is None:
        name = _DEFAULT_NAME
    path = data_path(f"displays/{name}.mat")
    if not path.exists():
        raise FileNotFoundError(f"Unknown display '{name}'")
    wave, spd, gamma = _load_display(path)
    return Display(spd=spd, wave=wave, gamma=gamma, name=name)
