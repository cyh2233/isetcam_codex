"""Load an :class:`Optics` from a MATLAB ``.mat`` file."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import numpy as np
from scipy.io import loadmat

from .optics_class import Optics


def _get_attr(obj: object, name: str):
    if isinstance(obj, dict):
        return obj.get(name)
    return getattr(obj, name, None)


def optics_from_file(path: str | Path, *, candidate_vars: Iterable[str] | None = None) -> Optics:
    """Load ``path`` and return an :class:`Optics`.

    Parameters
    ----------
    path:
        MAT-file containing an optics structure.
    candidate_vars:
        Optional sequence of variable names to search for. Defaults to
        ``('optics',)``.
    """
    if candidate_vars is None:
        candidate_vars = ("optics",)

    mat = loadmat(str(Path(path)), squeeze_me=True, struct_as_record=False)

    opt_struct = None
    for key in candidate_vars:
        if key in mat:
            opt_struct = mat[key]
            break
    if opt_struct is None:
        raise KeyError("No optics structure found in file")

    f_number = float(_get_attr(opt_struct, "f_number"))
    f_length = float(_get_attr(opt_struct, "f_length"))
    wave = _get_attr(opt_struct, "wave")
    if wave is not None:
        wave = np.asarray(wave).reshape(-1)
    transmittance = _get_attr(opt_struct, "transmittance")
    if transmittance is not None:
        transmittance = np.asarray(transmittance, dtype=float)
    name = _get_attr(opt_struct, "name")
    if isinstance(name, np.ndarray):
        name = str(name.squeeze())

    return Optics(
        f_number=f_number,
        f_length=f_length,
        wave=wave,
        transmittance=transmittance,
        name=name,
    )
