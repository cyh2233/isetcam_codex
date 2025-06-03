# mypy: ignore-errors
"""Create a frequency/orientation target scene."""

from __future__ import annotations

import numpy as np

from .scene_class import Scene
from ..energy_to_quanta import energy_to_quanta
from .imgtargets import img_fo_target

_DEF_WAVE = np.arange(400, 701, 10, dtype=float)


def _default_params() -> dict:
    return {
        "angles": np.linspace(0, np.pi / 2, 8),
        "freqs": np.arange(1, 9),
        "block_size": 32,
        "contrast": 1.0,
    }


def scene_freq_orient(params: dict | None = None) -> Scene:
    """Return a frequency/orientation target scene.

    Parameters
    ----------
    params : dict, optional
        Dictionary with optional keys ``"angles"``, ``"freqs"``,
        ``"block_size"`` and ``"contrast"`` controlling the target
        generation. Any missing key uses a sensible default.
    """
    if params is None:
        params = _default_params()
    else:
        d = _default_params()
        d.update(params)
        params = d

    img = img_fo_target(
        pattern="sine",
        angles=params["angles"],
        freqs=params["freqs"],
        block_size=int(params["block_size"]),
        contrast=float(params["contrast"]),
    )

    img = img / img.max()
    ill_photons = energy_to_quanta(_DEF_WAVE, np.ones_like(_DEF_WAVE)).ravel()
    photons = img[:, :, None] * ill_photons[None, None, :]

    sc = Scene(photons=photons, wave=_DEF_WAVE, name="FOTarget")
    sc.illuminant = ill_photons
    return sc


__all__ = ["scene_freq_orient"]
