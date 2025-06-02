# mypy: ignore-errors
"""Convert legacy illuminant structures to :class:`Illuminant`."""

from __future__ import annotations

from typing import Any

import numpy as np

from .illuminant_class import Illuminant


def _get(obj: Any, attr: str) -> Any:
    if isinstance(obj, dict):
        return obj.get(attr)
    return getattr(obj, attr, None)


def illuminant_modernize(illuminant: Any) -> Illuminant:
    """Return ``illuminant`` in modern :class:`Illuminant` form.

    Parameters
    ----------
    illuminant : Any
        Either an :class:`Illuminant` instance or a legacy structure that
        stores the spectral distribution in ``data`` or ``spd`` and the
        wavelength samples in ``wavelength`` or ``wave``.
    """
    if isinstance(illuminant, Illuminant):
        return illuminant

    # Attempt to detect modern attributes first
    spd = _get(illuminant, "spd")
    wave = _get(illuminant, "wave")
    if spd is not None and wave is not None:
        name = _get(illuminant, "name")
        return Illuminant(
            spd=np.asarray(spd, dtype=float).reshape(-1),
            wave=np.asarray(wave, dtype=float).reshape(-1),
            name=None if name is None else str(name),
        )

    # Legacy fields
    data = _get(illuminant, "data")
    if spd is None:
        if isinstance(data, dict):
            spd = data.get("photons")
        else:
            spd = getattr(data, "photons", None)
        if spd is None and data is not None:
            spd = data
    if spd is None:
        raise KeyError("Illuminant structure has no spectral data")

    wave = wave or _get(illuminant, "wavelength")
    if wave is None:
        spec = _get(illuminant, "spectrum")
        if spec is not None:
            wave = _get(spec, "wave")
    if wave is None:
        raise KeyError("Illuminant structure has no wavelength information")

    name = _get(illuminant, "name")

    return Illuminant(
        spd=np.asarray(spd, dtype=float).reshape(-1),
        wave=np.asarray(wave, dtype=float).reshape(-1),
        name=None if name is None else str(name),
    )
