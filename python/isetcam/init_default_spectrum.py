# mypy: ignore-errors
"""Utility for initializing wavelength sampling on dataclass objects."""

from __future__ import annotations

from typing import Any

import numpy as np


def init_default_spectrum(
    obj: Any,
    spectral_type: str = "multispectral",
    wave: np.ndarray | None = None,
) -> Any:
    """Set default wavelength samples for ``obj`` and return it.

    Parameters
    ----------
    obj : dataclass instance
        Object with a ``wave`` attribute that will be updated.
    spectral_type : {'multispectral', 'monochrome', 'custom'}, optional
        Defines the type of spectrum to assign. ``'multispectral'``
        uses a 400--700 nm range in 10 nm steps. ``'monochrome'``
        assigns a single wavelength (550 nm by default). ``'custom'``
        uses the provided ``wave`` values.
    wave : array-like, optional
        Custom wavelength samples used when ``spectral_type`` is
        ``'custom'`` or to override the defaults.

    Returns
    -------
    obj
        The updated dataclass instance.
    """
    if not hasattr(obj, "wave"):
        raise AttributeError("Object must have a 'wave' attribute")

    stype = spectral_type.lower()
    if stype == "multispectral":
        w = np.arange(400, 701, 10, dtype=float) if wave is None else np.asarray(wave, dtype=float)  # noqa: E501
    elif stype == "monochrome":
        if wave is None:
            w = np.array([550.0], dtype=float)
        else:
            w = np.asarray(wave, dtype=float).reshape(-1)
            if w.size != 1:
                raise ValueError("Monochrome spectrum must contain a single wavelength")
    elif stype == "custom":
        if wave is None:
            raise ValueError("wave must be provided for custom spectral type")
        w = np.asarray(wave, dtype=float)
    else:
        raise ValueError(f"Unknown spectral_type '{spectral_type}'")

    obj.wave = w
    return obj
