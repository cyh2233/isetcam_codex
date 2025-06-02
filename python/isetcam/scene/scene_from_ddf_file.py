# mypy: ignore-errors
"""Read a DDF file and return a :class:`Scene`."""

from __future__ import annotations

from pathlib import Path
import json
import io
from zipfile import ZipFile

import numpy as np

from .scene_class import Scene


def scene_from_ddf_file(path: str | Path) -> Scene:
    """Load ``path`` and return a :class:`Scene`.

    The ``.ddf`` file is expected to be a zip archive containing the files
    ``metadata.json``, ``photons.npy`` and ``wave.npy``. The metadata file is
    ignored except for verifying the cube dimensions.
    """
    path = Path(path)
    with ZipFile(path, 'r') as z:
        with z.open('metadata.json') as f:
            meta = json.load(f)
        with z.open('photons.npy') as f:
            photons = np.load(io.BytesIO(f.read()))
        with z.open('wave.npy') as f:
            wave = np.load(io.BytesIO(f.read()))

    photons = np.asarray(photons, dtype=float)
    wave = np.asarray(wave).reshape(-1)

    if photons.shape[2] != meta.get('nwave'):
        raise ValueError('metadata mismatch')
    if photons.shape[0] != meta.get('height') or photons.shape[1] != meta.get('width'):
        raise ValueError('metadata mismatch')

    return Scene(photons=photons, wave=wave)

