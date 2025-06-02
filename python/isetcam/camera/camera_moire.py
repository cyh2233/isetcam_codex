# mypy: ignore-errors
"""Generate moir\u00e9 pattern response of a camera."""

from __future__ import annotations

import numpy as np

from .camera_class import Camera
from .camera_compute import camera_compute
from ..scene import Scene


_DEF_SIZE = 256


def _moire_target(size: int = _DEF_SIZE, f: float | None = None) -> np.ndarray:
    """Return a radial sinusoidal pattern used for moir\u00e9 testing."""
    if f is None:
        f = 1.0 / size / 10.0
    y, x = np.mgrid[0:size, 0:size]
    dist2 = x.astype(float) ** 2 + y.astype(float) ** 2
    pattern = np.sin(np.pi * f * dist2)
    pattern = (pattern - pattern.min()) / (pattern.max() - pattern.min())
    return pattern


def camera_moire(camera: Camera, *, size: int = _DEF_SIZE,
                 f: float | None = None) -> tuple[np.ndarray, Camera]:
    """Simulate imaging a moir\u00e9 target with ``camera``.

    Parameters
    ----------
    camera : Camera
        Camera instance to evaluate.
    size : int, optional
        Size in pixels of the square moir\u00e9 scene. Default is ``256``.
    f : float, optional
        Spatial frequency scale factor for the target. When ``None`` a
        reasonable default based on ``size`` is used.

    Returns
    -------
    pattern : np.ndarray
        Sensor voltage image produced by the camera.
    Camera
        Updated camera with computed sensor voltages.
    """
    pattern = _moire_target(size, f)
    wave = camera.sensor.wave
    n_wave = wave.size if wave is not None else 1
    photons = np.repeat(pattern[:, :, None], n_wave, axis=2)
    scene = Scene(photons=photons, wave=wave, name="Moire")

    camera_compute(camera, scene)
    return camera.sensor.volts.copy(), camera


__all__ = ["camera_moire"]
