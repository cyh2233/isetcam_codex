# mypy: ignore-errors
"""Load an :class:`Illuminant` from a MATLAB ``.mat`` file."""

from __future__ import annotations

from pathlib import Path

import numpy as np
from scipy.io import loadmat

from .illuminant_class import Illuminant


def illuminant_from_file(path: str | Path) -> Illuminant:
    """Load ``path`` and return an :class:`Illuminant`.

    Parameters
    ----------
    path : str or Path
        MAT-file containing ``spd`` and ``wavelength`` variables.
    """
    mat = loadmat(str(Path(path)), squeeze_me=True, struct_as_record=False)
    if "spd" not in mat or "wavelength" not in mat:
        raise KeyError("File must contain 'spd' and 'wavelength'")

    spd = np.asarray(mat["spd"], dtype=float).reshape(-1)
    wave = np.asarray(mat["wavelength"], dtype=float).reshape(-1)
    name = mat.get("name")
    if isinstance(name, np.ndarray):
        name = str(name.squeeze())

    return Illuminant(spd=spd, wave=wave, name=name)
