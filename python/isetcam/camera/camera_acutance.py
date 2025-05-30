from __future__ import annotations

import numpy as np

from .camera_class import Camera
from .camera_mtf import camera_mtf
from ..metrics import iso_acutance


_DEF_F_LENGTH = 0.004  # meters


def _freq_to_cpd(freq: np.ndarray, f_length: float) -> np.ndarray:
    deg_per_mm = (1e-3 / f_length) * 180.0 / np.pi
    return freq / deg_per_mm


def camera_acutance(camera: Camera) -> float:
    """Return the ISO acutance of ``camera``."""
    freqs, mtf = camera_mtf(camera)
    f_length = getattr(camera.optics, "f_length", _DEF_F_LENGTH)
    cpd = _freq_to_cpd(freqs, f_length)
    return iso_acutance(cpd, mtf)


__all__ = ["camera_acutance"]
