"""Create a Scene from an image file."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import numpy as np
import imageio.v2 as imageio

from ..luminance_from_energy import luminance_from_energy
from .scene_class import Scene


def scene_from_file(
    path: str | Path,
    mean_luminance: Optional[float] = None,
    wave: Optional[np.ndarray] = None,
) -> Scene:
    """Read ``path`` and return a :class:`Scene`.

    Parameters
    ----------
    path : str or Path
        Location of the image file to read.
    mean_luminance : float, optional
        When provided, scale the image so that its mean luminance equals this
        value.
    wave : array-like, optional
        Wavelength samples in nanometers. If omitted, a simple sequence
        ``np.arange(n_channels)`` is used.

    Returns
    -------
    Scene
        Scene containing the image data.
    """
    img = imageio.imread(Path(path))
    data = np.asarray(img, dtype=float)
    if data.ndim == 2:
        data = data[:, :, np.newaxis]

    if wave is None:
        wave = np.arange(data.shape[2])
    wave = np.asarray(wave).reshape(-1)
    if len(wave) != data.shape[2]:
        raise ValueError("wave must match number of image channels")

    if mean_luminance is not None:
        lum = luminance_from_energy(data, wave)
        current_mean = float(lum.mean())
        if current_mean > 0:
            data = data * (mean_luminance / current_mean)

    return Scene(photons=data, wave=wave)
