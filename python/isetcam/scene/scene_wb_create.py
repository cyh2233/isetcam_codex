# mypy: ignore-errors
"""Create individual wavelength scene files."""

from __future__ import annotations

from pathlib import Path
from typing import Optional, List

import numpy as np
from scipy.io import savemat

from .scene_class import Scene
from .scene_to_file import scene_to_file
from .scene_create import _load_macbeth_data
from ..illuminant import illuminant_create


def _default_scene(patch_size: int, illuminant: str) -> Scene:
    illum = illuminant_create(illuminant)
    refl, wave = _load_macbeth_data(illum.wave)
    nrows, ncols = 4, 6
    photons = np.zeros((patch_size * nrows, patch_size * ncols, wave.size), dtype=float)
    idx = 0
    for r in range(nrows):
        for c in range(ncols):
            patch = refl[:, idx] * illum.spd
            photons[r * patch_size:(r + 1) * patch_size,
                    c * patch_size:(c + 1) * patch_size, :] = patch
            idx += 1
    name = f"Macbeth {illum.name}" if illum.name else "Macbeth"
    return Scene(photons=photons, wave=wave, name=name)


def scene_wb_create(
    scene: Optional[Scene] = None,
    work_dir: Optional[str | Path] = None,
    *,
    patch_size: int = 16,
    illuminant: str = "D65",
) -> List[Path]:
    """Write ``scene`` as a series of single-wavelength MAT-files.

    When ``scene`` is omitted, a Macbeth ColorChecker is generated using the
    specified ``patch_size`` and ``illuminant`` before splitting.

    Parameters
    ----------
    scene : Scene, optional
        Scene to split. If ``None``, a Macbeth chart is created.
    work_dir : str or Path, optional
        Destination directory for the files. If not provided, a directory named
        after the scene is created in the current working directory.
    patch_size : int, optional
        Size of each Macbeth patch when creating the default scene.
    illuminant : str, optional
        Illuminant name used when creating the default scene. ``"D65"`` is the
        default.

    Returns
    -------
    list of Path
        Paths to the MAT-files created.
    """

    if scene is None:
        scene = _default_scene(patch_size, illuminant)
    if not isinstance(scene, Scene):
        raise TypeError("scene must be a Scene")

    if work_dir is None:
        name = scene.name or "scene"
        work_dir = Path.cwd() / name.replace(" ", "_")
    else:
        work_dir = Path(work_dir)
    work_dir.mkdir(parents=True, exist_ok=True)

    paths: List[Path] = []
    for idx, w in enumerate(scene.wave):
        sub = Scene(
            photons=scene.photons[:, :, idx:idx + 1].copy(),
            wave=np.array([float(w)], dtype=float),
            name=scene.name,
        )
        fname = f"scene{int(round(float(w)))}.mat"
        path = work_dir / fname
        savemat(str(path), {"scene": {"photons": sub.photons, "wave": sub.wave}})
        paths.append(path)
    return paths
