"""Create a thumbnail RGB image for a :class:`Scene`."""

from __future__ import annotations

import numpy as np
from skimage.transform import resize

from .scene_class import Scene
from ..ie_xyz_from_photons import ie_xyz_from_photons
from ..srgb_xyz import xyz_to_srgb


def scene_thumbnail(scene: Scene, size: tuple[int, int] = (128, 128)) -> np.ndarray:
    """Return a downscaled sRGB rendering of ``scene``.

    Parameters
    ----------
    scene : Scene
        Scene to render.
    size : tuple[int, int], optional
        Desired ``(rows, cols)`` for the output thumbnail. Defaults to ``(128, 128)``.

    Returns
    -------
    np.ndarray
        sRGB image of shape ``(rows, cols, 3)`` with values in ``[0, 1]``.
    """
    xyz = ie_xyz_from_photons(scene.photons, scene.wave)
    srgb, _, _ = xyz_to_srgb(xyz)
    img = np.clip(srgb, 0.0, 1.0)
    rows, cols = int(size[0]), int(size[1])
    thumb = resize(img, (rows, cols, 3), order=1, mode="reflect", anti_aliasing=True, preserve_range=True)
    return thumb.astype(float)
