"""Simplified human optical image computation."""

from __future__ import annotations

import numpy as np
from scipy.signal import fftconvolve

from ..scene import Scene
from ..optics import Optics, optics_cos4th, optics_otf
from ..opticalimage import (
    OpticalImage,
    oi_spatial_support,
    oi_calculate_irradiance,
    oi_calculate_illuminance,
)
from .human_otf import human_otf


_DEF_FNUMBER = 4.0
_DEF_FLENGTH = 0.017  # meters


def human_oi(scene: Scene, oi: OpticalImage | None = None) -> OpticalImage:
    """Return a human optical image computed from ``scene``."""
    if scene is None:
        raise ValueError("scene is required")

    if oi is None:
        photons = np.asarray(scene.photons, dtype=float).copy()
        oi = OpticalImage(photons=photons, wave=np.asarray(scene.wave, dtype=float))
    else:
        oi.photons = np.asarray(scene.photons, dtype=float).copy()
        oi.wave = np.asarray(scene.wave, dtype=float).copy()

    if hasattr(scene, "fov"):
        oi.wangular = scene.fov

    spacing = getattr(scene, "sample_spacing", 1.0)
    oi.sample_spacing = spacing

    sup = oi_spatial_support(oi, units="meters")
    X, Y = np.meshgrid(sup["x"], sup["y"])
    diag = np.sqrt(np.ptp(sup["x"]) ** 2 + np.ptp(sup["y"]) ** 2)
    fall = optics_cos4th(X, Y, _DEF_FLENGTH, diag, _DEF_FNUMBER, magnification=0)
    oi.photons *= fall[..., np.newaxis]

    otf, _, wave = human_otf(wave=oi.wave)
    psf = optics_otf(otf)
    for i in range(wave.size):
        oi.photons[:, :, i] = fftconvolve(
            oi.photons[:, :, i], psf[:, :, i], mode="same"
        )

    oi.irradiance = oi_calculate_irradiance(oi)
    oi.illuminance = oi_calculate_illuminance(oi)
    return oi
