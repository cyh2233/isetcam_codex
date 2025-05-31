"""Interpolate a :class:`Scene` to a new wavelength sampling."""

from __future__ import annotations

from typing import Sequence

import numpy as np

from .scene_class import Scene
from ..illuminant.illuminant_class import Illuminant


def scene_interpolate_w(scene: Scene, wave: Sequence[float]) -> Scene:
    """Return ``scene`` data interpolated to ``wave``.

    Parameters
    ----------
    scene : Scene
        Input scene to interpolate.
    wave : sequence of float
        Desired wavelength samples in nanometers.

    Returns
    -------
    Scene
        New scene resampled to ``wave``.
    """

    src_wave = np.asarray(scene.wave, dtype=float).reshape(-1)
    tgt_wave = np.asarray(wave, dtype=float).reshape(-1)

    photons = np.asarray(scene.photons, dtype=float)
    if photons.shape[-1] != src_wave.size:
        raise ValueError("scene.wave length must match photons shape")

    flat = photons.reshape(-1, src_wave.size)
    interp = np.empty((flat.shape[0], tgt_wave.size), dtype=float)
    for i, spec in enumerate(flat):
        interp[i] = np.interp(tgt_wave, src_wave, spec, left=0.0, right=0.0)
    new_photons = interp.reshape(photons.shape[0], photons.shape[1], tgt_wave.size)

    out = Scene(photons=new_photons, wave=tgt_wave, name=scene.name)

    # Copy other attributes
    for attr, val in scene.__dict__.items():
        if attr in {"photons", "wave", "name", "illuminant"}:
            continue
        setattr(out, attr, val)

    illum = getattr(scene, "illuminant", None)
    if illum is not None:
        if isinstance(illum, Illuminant):
            spd = np.asarray(illum.spd, dtype=float)
            i_wave = np.asarray(illum.wave, dtype=float)
            new_spd = np.interp(tgt_wave, i_wave, spd, left=0.0, right=0.0)
            out.illuminant = Illuminant(spd=new_spd, wave=tgt_wave, name=illum.name)
        else:
            ill = np.asarray(illum, dtype=float)
            if ill.ndim == 1:
                if ill.size != src_wave.size:
                    raise ValueError("Illuminant vector length must match scene wave")
                out.illuminant = np.interp(tgt_wave, src_wave, ill, left=0.0, right=0.0)
            elif ill.ndim == 3:
                if ill.shape != photons.shape:
                    raise ValueError("Illuminant cube must match scene photon shape")
                flat = ill.reshape(-1, src_wave.size)
                interp_ill = np.empty((flat.shape[0], tgt_wave.size), dtype=float)
                for i, spec in enumerate(flat):
                    interp_ill[i] = np.interp(tgt_wave, src_wave, spec, left=0.0, right=0.0)
                out.illuminant = interp_ill.reshape(ill.shape[0], ill.shape[1], tgt_wave.size)
            else:
                raise ValueError("Illuminant must be 1-D or 3-D or Illuminant object")

    return out


__all__ = ["scene_interpolate_w"]
