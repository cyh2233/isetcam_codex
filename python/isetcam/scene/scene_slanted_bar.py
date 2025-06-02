# mypy: ignore-errors
"""Create a slanted bar test scene."""

from __future__ import annotations

import numpy as np

from .scene_class import Scene
from ..energy_to_quanta import energy_to_quanta
from .imgtargets.img_slanted_bar import img_slanted_bar

_DEF_WAVE = np.arange(400, 701, 10, dtype=float)


def scene_slanted_bar(
    im_size: int = 384,
    bar_slope: float = 2.6,
    field_of_view: float = 2.0,
    wave: np.ndarray | None = None,
) -> Scene:
    """Return a slanted bar scene used for resolution testing.

    Parameters
    ----------
    im_size : int, optional
        Approximate size of the square image in pixels. Defaults to ``384``.
    bar_slope : float, optional
        Slope of the separating line ``y = bar_slope * x``. Defaults to ``2.6``.
    field_of_view : float, optional
        Horizontal field of view of the scene in degrees. Defaults to ``2``.
    wave : array-like, optional
        Wavelength samples in nanometers. Defaults to ``400:10:700``.
    """
    if wave is None:
        wave = _DEF_WAVE
    else:
        wave = np.asarray(wave, dtype=float)

    pattern = img_slanted_bar(im_size=im_size, bar_slope=bar_slope)
    ill_photons = energy_to_quanta(wave, np.ones_like(wave)).ravel()
    photons = pattern[:, :, None] * ill_photons[None, None, :]

    sc = Scene(photons=photons, wave=wave, name="slantedBar")
    sc.fov = float(field_of_view)
    sc.illuminant = ill_photons
    return sc


__all__ = ["scene_slanted_bar"]
