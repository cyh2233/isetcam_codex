# mypy: ignore-errors
"""Adjust the illuminant of a :class:`Scene`."""

from __future__ import annotations

from pathlib import Path
from typing import Union

import numpy as np
from scipy.io import loadmat

from .scene_class import Scene
from ..luminance_from_photons import luminance_from_photons


def _load_spd(path: Path) -> tuple[np.ndarray, np.ndarray | None]:
    """Return spectral data and wavelength from ``path``."""
    mat = loadmat(str(path))
    if "data" not in mat:
        raise KeyError("MAT-file must contain 'data'")
    spd = np.asarray(mat["data"], dtype=float).reshape(-1)
    wave = None
    if "wavelength" in mat:
        wave = np.asarray(mat["wavelength"], dtype=float).reshape(-1)
    elif "wave" in mat:
        wave = np.asarray(mat["wave"], dtype=float).reshape(-1)
    return spd, wave


def scene_adjust_illuminant(
    scene: Scene, illuminant: Union[np.ndarray, str, Path], preserve_mean: bool = True
) -> Scene:
    """Scale ``scene`` photon data by ``illuminant``.

    Parameters
    ----------
    scene : Scene
        Input scene to adjust.
    illuminant : array-like or path-like
        Spectral power distribution to apply. A path should point to a
        MATLAB ``.mat`` file containing ``wavelength`` and ``data`` arrays.
    preserve_mean : bool, optional
        When ``True`` (default) the mean luminance of ``scene`` is
        preserved after applying the illuminant.

    Returns
    -------
    Scene
        New scene with scaled photon data.
    """

    orig_mean = float(luminance_from_photons(scene.photons, scene.wave).mean())

    if isinstance(illuminant, (str, Path)):
        spd, wave = _load_spd(Path(illuminant))
        if wave is not None and not np.array_equal(wave, scene.wave):
            spd = np.interp(scene.wave, wave, spd, left=0.0, right=0.0)
    else:
        spd = np.asarray(illuminant, dtype=float).reshape(-1)
        if spd.size != len(scene.wave):
            raise ValueError("Illuminant vector length must match scene wave")

    photons = scene.photons * spd[np.newaxis, np.newaxis, :]

    if preserve_mean:
        new_mean = float(luminance_from_photons(photons, scene.wave).mean())
        if new_mean > 0:
            photons = photons * (orig_mean / new_mean)

    return Scene(photons=photons, wave=scene.wave, name=scene.name)
