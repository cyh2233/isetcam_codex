"""Factory function for :class:`Illuminant` objects."""

from __future__ import annotations

from pathlib import Path

import numpy as np
from scipy.io import loadmat

from ..data_path import data_path

from .illuminant_class import Illuminant


_DEF_DIR = 'data'


def _load_spd(path: Path) -> tuple[np.ndarray, np.ndarray]:
    data = loadmat(path)
    wave = data['wavelength'].ravel()
    spd = data['data'].ravel()
    return wave, spd


def illuminant_create(name: str, wave: np.ndarray | None = None) -> Illuminant:
    """Create an illuminant by name, optionally interpolated to ``wave``."""
    fname = name.strip().upper() + '.mat'
    path = data_path(f'lights/{fname}')
    if not path.exists():
        raise FileNotFoundError(f"Unknown illuminant '{name}'")
    src_wave, spd = _load_spd(path)
    if wave is not None:
        wave = np.asarray(wave, dtype=float)
        spd = np.interp(wave, src_wave, spd, left=0.0, right=0.0)
    else:
        wave = src_wave
    return Illuminant(spd=spd.astype(float), wave=wave, name=name)
