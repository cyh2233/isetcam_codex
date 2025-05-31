"""Load a :class:`VCImage` from a MATLAB ``.mat`` file."""

from __future__ import annotations

from pathlib import Path

import numpy as np
from scipy.io import loadmat

from .vcimage_class import VCImage


def ip_from_file(path: str | Path) -> VCImage:
    """Load ``path`` and return a :class:`VCImage`.

    Parameters
    ----------
    path : str or Path
        MAT-file containing ``rgb`` and ``wave`` variables.
    """
    mat = loadmat(str(Path(path)), squeeze_me=True, struct_as_record=False)
    if "rgb" not in mat or "wave" not in mat:
        raise KeyError("File must contain 'rgb' and 'wave'")

    rgb = np.asarray(mat["rgb"], dtype=float)
    wave = np.asarray(mat["wave"], dtype=float).reshape(-1)
    name = mat.get("name")
    if isinstance(name, np.ndarray):
        name = str(name.squeeze())

    return VCImage(rgb=rgb, wave=wave, name=name)
