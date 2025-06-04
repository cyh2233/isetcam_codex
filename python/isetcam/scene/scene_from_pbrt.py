# mypy: ignore-errors
"""Render a PBRT scene using ISET3D or a PBRT executable."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Tuple, Optional
import shutil
import subprocess

import numpy as np

from .scene_class import Scene
from ..opticalimage.oi_class import OpticalImage
from ..io import openexr_read

try:  # pragma: no cover - optional dependency
    import iset3d  # type: ignore
except Exception:  # pragma: no cover - library may not be present
    iset3d = None  # type: ignore


def _iset3d_available() -> bool:
    return iset3d is not None


def _pbrt_available() -> bool:
    return shutil.which("pbrt") is not None


def scene_from_pbrt(path_or_recipe: Any) -> Tuple[Scene, Optional[OpticalImage], dict]:
    """Render ``path_or_recipe`` and return a :class:`Scene`.

    The function relies on the optional `iset3d` package or a local `pbrt`
    executable.  When neither backend is available an :class:`ImportError`
    is raised.
    """
    if _iset3d_available():
        # The path can be a PBRT file or an iset3d recipe object
        if isinstance(path_or_recipe, (str, Path)):
            recipe = iset3d.piRead(str(Path(path_or_recipe)))
        else:
            recipe = path_or_recipe
        iset3d.piWrite(recipe)
        obj, *_ = iset3d.piRender(recipe, "render type", ["radiance", "depth"])
        photons = np.asarray(getattr(obj, "photons"))
        wave = np.asarray(getattr(obj, "wave")).reshape(-1)
        depth = getattr(obj, "depthMap", None)
        name = getattr(obj, "name", None)
        if getattr(obj, "type", "scene") == "scene":
            sc = Scene(photons=photons, wave=wave, name=name)
            if depth is not None:
                sc.depth_map = np.asarray(depth)
            return sc, None, {"depth": getattr(sc, "depth_map", None)}
        else:
            oi = OpticalImage(photons=photons, wave=wave, name=name)
            if depth is not None:
                oi.depth_map = np.asarray(depth)
            # Convert optical image to scene
            sc = Scene(photons=oi.photons, wave=oi.wave, name=oi.name)
            if depth is not None:
                sc.depth_map = np.asarray(depth)
            return sc, oi, {"depth": getattr(sc, "depth_map", None)}

    if _pbrt_available():
        pbrt = shutil.which("pbrt")
        assert pbrt is not None
        path = Path(path_or_recipe)
        subprocess.run([pbrt, str(path)], check=True)
        exr_path = path.with_suffix(".exr")
        channels = openexr_read(exr_path)
        if set(channels.keys()) >= {"R", "G", "B"}:
            photons = np.stack([channels["R"], channels["G"], channels["B"]], axis=2)
        else:
            key = next(iter(channels))
            photons = channels[key][:, :, None]
        sc = Scene(photons=photons)
        depth_exr = path.with_name(path.stem + "_depth.exr")
        if depth_exr.exists():
            depth_channels = openexr_read(depth_exr)
            if depth_channels:
                sc.depth_map = next(iter(depth_channels.values()))
        return sc, None, {"depth": getattr(sc, "depth_map", None)}

    raise ImportError("iset3d or pbrt backend required")


__all__ = ["scene_from_pbrt"]

