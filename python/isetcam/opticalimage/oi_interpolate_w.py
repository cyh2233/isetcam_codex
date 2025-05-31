"""Interpolate an :class:`OpticalImage` to a new wavelength sampling."""

from __future__ import annotations

from typing import Sequence

import numpy as np

from .oi_class import OpticalImage
from ..illuminant.illuminant_class import Illuminant


def oi_interpolate_w(oi: OpticalImage, wave: Sequence[float]) -> OpticalImage:
    """Return ``oi`` data interpolated to ``wave``."""

    src_wave = np.asarray(oi.wave, dtype=float).reshape(-1)
    tgt_wave = np.asarray(wave, dtype=float).reshape(-1)

    photons = np.asarray(oi.photons, dtype=float)
    if photons.shape[-1] != src_wave.size:
        raise ValueError("oi.wave length must match photons shape")

    flat = photons.reshape(-1, src_wave.size)
    interp = np.empty((flat.shape[0], tgt_wave.size), dtype=float)
    for i, spec in enumerate(flat):
        interp[i] = np.interp(tgt_wave, src_wave, spec, left=0.0, right=0.0)
    new_photons = interp.reshape(photons.shape[0], photons.shape[1], tgt_wave.size)

    out = OpticalImage(photons=new_photons, wave=tgt_wave, name=oi.name)

    for attr, val in oi.__dict__.items():
        if attr in {"photons", "wave", "name", "illuminant"}:
            continue
        setattr(out, attr, val)

    illum = getattr(oi, "illuminant", None)
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
                    raise ValueError("Illuminant vector length must match oi wave")
                out.illuminant = np.interp(tgt_wave, src_wave, ill, left=0.0, right=0.0)
            elif ill.ndim == 3:
                if ill.shape != photons.shape:
                    raise ValueError("Illuminant cube must match oi photon shape")
                flat = ill.reshape(-1, src_wave.size)
                interp_ill = np.empty((flat.shape[0], tgt_wave.size), dtype=float)
                for i, spec in enumerate(flat):
                    interp_ill[i] = np.interp(tgt_wave, src_wave, spec, left=0.0, right=0.0)
                out.illuminant = interp_ill.reshape(ill.shape[0], ill.shape[1], tgt_wave.size)
            else:
                raise ValueError("Illuminant must be 1-D or 3-D or Illuminant object")

    return out


__all__ = ["oi_interpolate_w"]
