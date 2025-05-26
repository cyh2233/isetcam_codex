"""Utilities for saving :class:`Optics` objects to disk."""

from __future__ import annotations

from pathlib import Path

from scipy.io import savemat

from .optics_class import Optics


def optics_to_file(optics: Optics, path: str | Path) -> None:
    """Save ``optics`` to ``path`` as a MATLAB ``.mat`` file.

    The structure is stored under the variable name ``'optics'``.
    """
    data = {
        "f_number": optics.f_number,
        "f_length": optics.f_length,
        "wave": optics.wave,
        "transmittance": optics.transmittance,
    }
    if optics.name is not None:
        data["name"] = optics.name
    savemat(str(Path(path)), {"optics": data})
