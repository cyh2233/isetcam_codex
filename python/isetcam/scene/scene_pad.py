# mypy: ignore-errors
"""Pad a Scene's photon data."""

from __future__ import annotations

from typing import Sequence

import numpy as np

from .scene_class import Scene


def scene_pad(scene: Scene, pad_size: int | Sequence[int], value: float = 0) -> Scene:
    """Pad ``scene`` by ``pad_size`` pixels on all sides.

    Parameters
    ----------
    scene : Scene
        Input scene to pad.
    pad_size : int or sequence of int
        Amount of padding. If an integer, the same value is used on all
        sides. If a sequence of two integers, the first specifies padding
        for the top and bottom, and the second for the left and right.
        A sequence of four integers specifies ``(top, bottom, left, right)``.
    value : float, optional
        Value used to fill the padded region. Defaults to 0.

    Returns
    -------
    Scene
        New scene containing the padded photon data with the same
        wavelength samples.
    """

    if isinstance(pad_size, Sequence):
        pad = list(pad_size)
        if len(pad) == 2:
            top = bottom = int(pad[0])
            left = right = int(pad[1])
        elif len(pad) == 4:
            top, bottom, left, right = [int(v) for v in pad]
        else:
            raise ValueError("pad_size must be a scalar or have length 2 or 4")
    else:
        top = bottom = left = right = int(pad_size)

    pad_width = ((top, bottom), (left, right), (0, 0))
    padded = np.pad(scene.photons, pad_width, mode="constant", constant_values=value)
    return Scene(photons=padded, wave=scene.wave, name=scene.name)
