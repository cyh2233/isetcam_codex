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


def display_create(name: str | None = None, wave: np.ndarray | None = None) -> Display:
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
    file_wave, spd, gamma = _load_display(path)
    if wave is not None:
        new_wave = np.asarray(wave, dtype=float).ravel()
        if len(new_wave) != len(file_wave):
            spd = np.column_stack(
                [np.interp(new_wave, file_wave, spd[:, i]) for i in range(spd.shape[1])]
            )
            if gamma is not None and gamma.shape[0] == len(file_wave):
                gamma = np.column_stack(
                    [np.interp(new_wave, file_wave, gamma[:, i]) for i in range(gamma.shape[1])]
                )
            file_wave = new_wave
    return Display(spd=spd, wave=file_wave, gamma=gamma, name=name)
