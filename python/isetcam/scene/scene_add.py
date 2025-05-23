"""Utilities for combining scene data."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence, Union, List

import numpy as np


@dataclass
class Scene:
    """Minimal representation of an ISETCam scene."""

    photons: np.ndarray
    wave: np.ndarray


SceneInput = Union[Scene, Sequence[Scene]]


def _remove_spatial_mean(data: np.ndarray) -> np.ndarray:
    """Remove the mean from each spectral band."""
    mean = data.mean(axis=(0, 1), keepdims=True)
    return data - mean


def scene_add(in1: SceneInput, in2: Union[Scene, Sequence[float]], add_flag: str = "add") -> Scene:
    """Combine scenes using the logic of MATLAB ``sceneAdd``.

    Parameters
    ----------
    in1 : Scene or sequence of Scene
        Primary scene or list of scenes.
    in2 : Scene or sequence of float
        Second scene to combine with ``in1`` or weights for ``in1`` when it is
        a sequence.
    add_flag : {"add", "average", "remove spatial mean"}, optional
        Defines how the scenes are combined.

    Returns
    -------
    Scene
        Resulting scene with combined photon data.
    """
    flag = add_flag.lower().replace(" ", "")

    if isinstance(in1, Sequence) and not isinstance(in1, Scene):
        scenes: List[Scene] = list(in1)
        weights = np.asarray(in2, dtype=float)
        if len(weights) != len(scenes):
            raise ValueError("Weight vector length must match number of scenes")
        wave = scenes[0].wave
        for sc in scenes[1:]:
            if not np.array_equal(sc.wave, wave):
                raise ValueError("All scenes must share the same wavelength")

        if flag == "average":
            total = np.zeros_like(scenes[0].photons, dtype=float)
            for sc in scenes:
                total += sc.photons
            photons = total / len(scenes)
        else:
            photons = weights[0] * scenes[0].photons
            for w, sc in zip(weights[1:], scenes[1:]):
                band = sc.photons
                if flag == "removespatialmean":
                    band = _remove_spatial_mean(band)
                elif flag != "add":
                    raise ValueError(f"Unknown add_flag {add_flag}")
                photons += w * band
        return Scene(photons=photons, wave=wave)

    # Pair of scenes
    if not isinstance(in1, Scene) or not isinstance(in2, Scene):
        raise TypeError("in1 and in2 must be Scene instances")
    if not np.array_equal(in1.wave, in2.wave):
        raise ValueError("Scenes must have matching wavelength samples")

    photons1 = in1.photons
    photons2 = in2.photons

    if flag == "add":
        photons = photons1 + photons2
    elif flag == "average":
        photons = (photons1 + photons2) / 2
    elif flag == "removespatialmean":
        photons = photons1 + _remove_spatial_mean(photons2)
    else:
        raise ValueError(f"Unknown add_flag {add_flag}")

    return Scene(photons=photons, wave=in1.wave)
