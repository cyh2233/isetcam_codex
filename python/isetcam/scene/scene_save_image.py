"""Save a rendered RGB version of a Scene."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import imageio.v2 as imageio

from .scene_class import Scene
from ..ie_xyz_from_photons import ie_xyz_from_photons
from ..srgb_xyz import xyz_to_srgb


def scene_save_image(scene: Scene, path: str | Path) -> None:
    """Save an sRGB rendering of ``scene`` to ``path``.

    Parameters
    ----------
    scene : Scene
        Scene to save.
    path : str or Path
        Destination image file path.
    """
    xyz = ie_xyz_from_photons(scene.photons, scene.wave)
    srgb, _, _ = xyz_to_srgb(xyz)
    img = np.clip(srgb, 0.0, 1.0)

    arr = (img * 255).round().astype(np.uint8)
    imageio.imwrite(str(Path(path)), arr)
