# mypy: ignore-errors
"""Compute an optical image from a scene and optics."""

from __future__ import annotations

import numpy as np

from ..scene import Scene
from ..optics import Optics
from .oi_class import OpticalImage


def oi_compute(scene: Scene, optics: Optics) -> OpticalImage:
    """Return the irradiance image formed by ``optics`` on ``scene``.

    This simplified model interpolates the scene radiance to the
    optics wavelength sampling, applies the optics transmittance and
    scales the result by ``(f_length / f_number)**2``.
    """

    sc_wave = np.asarray(scene.wave, dtype=float).reshape(-1)
    oi_wave = np.asarray(optics.wave, dtype=float).reshape(-1)

    photons = np.asarray(scene.photons, dtype=float)
    if photons.shape[-1] != sc_wave.size:
        raise ValueError("scene.wave length must match photons shape")

    flat = photons.reshape(-1, sc_wave.size)
    interp = np.empty((flat.shape[0], oi_wave.size), dtype=float)
    for i, spec in enumerate(flat):
        interp[i] = np.interp(oi_wave, sc_wave, spec, left=0.0, right=0.0)
    oi_photons = interp.reshape(photons.shape[0], photons.shape[1], oi_wave.size)

    trans = optics.transmittance
    if trans is None:
        trans = np.ones_like(oi_wave, dtype=float)
    else:
        trans = np.asarray(trans, dtype=float)
        if trans.size != oi_wave.size:
            raise ValueError("optics.transmittance length must match optics.wave")
    oi_photons *= trans

    scale = (float(optics.f_length) / float(optics.f_number)) ** 2
    oi_photons *= scale

    return OpticalImage(photons=oi_photons, wave=oi_wave, name=getattr(scene, "name", None))  # noqa: E501
