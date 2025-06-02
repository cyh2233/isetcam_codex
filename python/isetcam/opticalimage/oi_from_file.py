# mypy: ignore-errors
"""Load an :class:`OpticalImage` from a MATLAB ``.mat`` file."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import numpy as np
from scipy.io import loadmat

from .oi_class import OpticalImage


def _get_attr(obj: object, name: str):
    if isinstance(obj, dict):
        return obj.get(name)
    return getattr(obj, name, None)


def oi_from_file(path: str | Path, *, candidate_vars: Iterable[str] | None = None) -> OpticalImage:  # noqa: E501
    """Load ``path`` and return an :class:`OpticalImage`.

    Parameters
    ----------
    path:
        MAT-file containing an optical image structure.
    candidate_vars:
        Optional sequence of variable names to search for. Defaults to
        ``('oi', 'opticalimage')``.
    """
    if candidate_vars is None:
        candidate_vars = ("oi", "opticalimage")

    mat = loadmat(str(Path(path)), squeeze_me=True, struct_as_record=False)

    oi_struct = None
    for key in candidate_vars:
        if key in mat:
            oi_struct = mat[key]
            break
    if oi_struct is None:
        raise KeyError("No optical image structure found in file")

    photons = np.asarray(_get_attr(oi_struct, "photons"))
    wave = _get_attr(oi_struct, "wave")
    if wave is not None:
        wave = np.asarray(wave).reshape(-1)
    name = _get_attr(oi_struct, "name")
    if isinstance(name, np.ndarray):
        name = str(name.squeeze())

    return OpticalImage(photons=photons, wave=wave, name=name)
