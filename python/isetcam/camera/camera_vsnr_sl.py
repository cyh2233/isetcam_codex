# mypy: ignore-errors
"""Compute VSNR across luminance levels using a camera model."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np

from .camera_class import Camera
from .camera_compute import camera_compute
from ..scene import Scene, scene_adjust_luminance
from ..quanta2energy import quanta_to_energy
from ..ie_xyz_from_energy import ie_xyz_from_energy
from ..metrics import xyz_to_vsnr


_DEFAULT_LEVELS = np.array([3, 6, 12, 25, 50, 100, 200, 400], dtype=float)


@dataclass
class VSNRSLResult:
    """Container for VSNR sweep results."""

    vsnr: np.ndarray
    mean_luminances: np.ndarray


_DEF_SCENE_WAVE = np.array([500.0, 510.0, 520.0], dtype=float)
_DEF_SCENE_PHOTONS = np.ones((4, 4, _DEF_SCENE_WAVE.size), dtype=float)


def _base_scene() -> Scene:
    """Return a small uniform scene used for testing."""
    return Scene(photons=_DEF_SCENE_PHOTONS.copy(), wave=_DEF_SCENE_WAVE.copy())


def camera_vsnr_sl(
    camera: Camera, mean_luminances: Sequence[float] | None = None
) -> VSNRSLResult:
    """Return VSNR values over several luminance levels."""

    if mean_luminances is None:
        levels = _DEFAULT_LEVELS
    else:
        levels = np.asarray(mean_luminances, dtype=float).reshape(-1)

    vsnr_vals = np.zeros(levels.size, dtype=float)

    for i, lum in enumerate(levels):
        scene = _base_scene()
        scene = scene_adjust_luminance(scene, "mean", float(lum))
        camera_compute(camera, scene)
        energy = quanta_to_energy(scene.wave, scene.photons)
        xyz = ie_xyz_from_energy(energy, scene.wave)
        vsnr_vals[i] = float(xyz_to_vsnr(xyz, np.array([1.0, 1.0, 1.0])))

    return VSNRSLResult(vsnr=vsnr_vals, mean_luminances=levels)


__all__ = ["camera_vsnr_sl", "VSNRSLResult"]
