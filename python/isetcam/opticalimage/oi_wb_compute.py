# mypy: ignore-errors
"""Compute and save single-wavelength optical images."""

from __future__ import annotations

from pathlib import Path
from typing import Optional, List

import numpy as np
from scipy.io import loadmat

from .oi_class import OpticalImage
from .oi_compute import oi_compute
from .oi_to_file import oi_to_file
from ..scene import Scene
from ..optics import Optics, optics_create


def _get_attr(obj: object, name: str):
    if isinstance(obj, dict):
        return obj.get(name)
    return getattr(obj, name, None)


def _load_scene(path: Path) -> Scene:
    mat = loadmat(str(path), squeeze_me=True, struct_as_record=False)
    sc_struct = mat.get("scene")
    if sc_struct is None:
        raise KeyError("No scene structure found in file")
    photons = np.asarray(_get_attr(sc_struct, "photons"), dtype=float)
    if photons.ndim == 2:
        photons = photons[:, :, np.newaxis]
    wave = _get_attr(sc_struct, "wave")
    if wave is not None:
        wave = np.asarray(wave, dtype=float).reshape(-1)
    name = _get_attr(sc_struct, "name")
    if isinstance(name, np.ndarray):
        name = str(name.squeeze())
    return Scene(photons=photons, wave=wave, name=name)


def _single_wave_optics(template: Optics, wave: np.ndarray) -> Optics:
    trans = template.transmittance
    if trans is not None:
        trans = np.asarray(trans, dtype=float)
        if trans.size > 1 and template.wave.size > 1:
            value = np.interp(float(wave[0]), template.wave, trans, left=trans[0], right=trans[-1])
            trans = np.array([float(value)], dtype=float)
        else:
            trans = trans.reshape(-1)[:1]
    return Optics(
        f_number=float(template.f_number),
        f_length=float(template.f_length),
        wave=np.asarray(wave, dtype=float).reshape(-1),
        transmittance=trans,
        name=template.name,
    )


def oi_wb_compute(directory: str | Path, oi: Optional[Optics] = None) -> List[Path]:
    """Compute optical images for each ``scene*.mat`` in ``directory``.

    Each scene file is loaded, processed with :func:`oi_compute`, and the
    resulting optical image is saved as ``oi<wave>.mat`` within the same
    directory via :func:`oi_to_file`.
    """
    work_dir = Path(directory)
    if oi is None:
        template = optics_create()
    else:
        if not isinstance(oi, Optics):
            raise TypeError("oi must be an Optics instance")
        template = oi

    paths: List[Path] = []
    for sc_path in sorted(work_dir.glob("scene*.mat")):
        scene = _load_scene(sc_path)
        optics = _single_wave_optics(template, scene.wave)
        out_oi = oi_compute(scene, optics)
        fname = f"oi{int(round(float(scene.wave[0])))}.mat"
        out_path = work_dir / fname
        oi_to_file(out_oi, out_path)
        paths.append(out_path)
    return paths


__all__ = ["oi_wb_compute"]
