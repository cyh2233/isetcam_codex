# mypy: ignore-errors
"""Convert a ctToolbox display definition to a :class:`Display`."""

from __future__ import annotations

from pathlib import Path
from typing import Mapping, Sequence

import numpy as np

from .display_class import Display
from .display_to_file import display_to_file


def _parse_ct_dict(ct_disp: Mapping) -> tuple[np.ndarray, np.ndarray, np.ndarray, str | None]:
    """Extract wave, spd, gamma and name from a toolbox dictionary."""
    name = ct_disp.get("m_strDisplayName")
    phys = ct_disp.get("sPhysicalDisplay", {})
    dixel = phys.get("m_objCDixelStructure", {})

    wave = np.asarray(dixel.get("m_aWaveLengthSamples"), dtype=float).ravel()
    spd = np.asarray(dixel.get("m_aSpectrumOfPrimaries"), dtype=float)
    if spd.ndim == 2 and spd.shape[0] != wave.size:
        spd = spd.T

    gamma_list = dixel.get("m_cellGammaStructure", [])
    if isinstance(gamma_list, Mapping):
        gamma_list = [gamma_list]
    gamma = np.column_stack([np.asarray(g["vGammaRampLUT"], dtype=float).ravel() for g in gamma_list]) if gamma_list else None

    return wave, spd, gamma, name


def display_convert(
    ct_disp: Mapping,
    wave: Sequence[float] | None = None,
    out_file: str | Path | None = None,
    overwrite: bool = False,
    name: str | None = None,
) -> Display:
    """Convert ``ct_disp`` to a :class:`Display` instance."""

    cwave, cspd, cgamma, cname = _parse_ct_dict(ct_disp)

    if wave is not None:
        wave = np.asarray(wave, dtype=float).ravel()
        cspd = np.array([np.interp(wave, cwave, cspd[:, i]) for i in range(cspd.shape[1])]).T
        cwave = wave

    if name is not None:
        cname = name

    disp = Display(spd=cspd, wave=cwave, gamma=cgamma, name=cname)

    if out_file is not None:
        path = Path(out_file)
        if path.exists() and not overwrite:
            raise FileExistsError(path)
        display_to_file(disp, path)

    return disp


__all__ = ["display_convert"]
