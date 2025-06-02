# mypy: ignore-errors
"""Extract a subset of wavelengths from a :class:`Scene`."""

from __future__ import annotations

from typing import Sequence

import numpy as np

from .scene_class import Scene


def scene_extract_waveband(scene: Scene, wave_list: Sequence[float]) -> Scene:
    """Return a new scene containing only wavelengths in ``wave_list``.

    Parameters
    ----------
    scene : Scene
        Input scene to subset.
    wave_list : sequence of float
        Wavelengths in nanometers to extract from ``scene``.

    Returns
    -------
    Scene
        Scene with photon data restricted to the requested wavelengths.
    """

    wv = np.asarray(scene.wave, dtype=float).reshape(-1)
    target = np.asarray(wave_list, dtype=float).reshape(-1)

    indices = []
    for w in target:
        matches = np.where(np.isclose(wv, w))[0]
        if matches.size == 0:
            raise ValueError(f"Wavelength {w} not found in scene.wave")
        indices.append(matches[0])

    photons = scene.photons[:, :, indices].copy()
    new_wave = wv[indices]
    return Scene(photons=photons, wave=new_wave, name=scene.name)
