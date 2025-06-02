# mypy: ignore-errors
"""Factory function for :class:`Optics` objects."""

from __future__ import annotations

from typing import Optional

import numpy as np

from .optics_class import Optics


_DEF_FNUMBER = 4.0
_DEF_FLENGTH = 0.004  # 4 mm


def optics_create(name: str = "default", wave: Optional[np.ndarray] = None) -> Optics:
    """Create an :class:`Optics` by ``name``."""
    flag = name.lower().replace(" ", "")
    if flag in {"default", "diffractionlimited"}:
        trans = None
    elif flag == "diffuser":
        trans = 0.5
    else:
        raise ValueError(f"Unknown optics type '{name}'")

    if trans is None:
        optics = Optics(f_number=_DEF_FNUMBER, f_length=_DEF_FLENGTH, wave=wave, name=name)  # noqa: E501
    else:
        if wave is None:
            optics = Optics(f_number=_DEF_FNUMBER, f_length=_DEF_FLENGTH, wave=None, name=name)  # noqa: E501
            optics.transmittance *= trans
        else:
            wave_arr = np.asarray(wave, dtype=float).reshape(-1)
            optics = Optics(f_number=_DEF_FNUMBER, f_length=_DEF_FLENGTH, wave=wave_arr,
                            transmittance=np.full(wave_arr.shape, trans, dtype=float), name=name)  # noqa: E501
    return optics
