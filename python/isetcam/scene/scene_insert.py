"""Insert one scene into another."""

from __future__ import annotations

from typing import Sequence

import numpy as np

from .scene_class import Scene
from .scene_utils import get_photons


def scene_insert(
    base_scene: Scene, insert_scene: Scene, location: Sequence[int]
) -> Scene:
    """Overlay ``insert_scene`` onto ``base_scene`` starting at ``location``.

    Parameters
    ----------
    base_scene : Scene
        Scene providing the background photon data.
    insert_scene : Scene
        Scene to insert. Must share the same wavelength samples as
        ``base_scene``.
    location : sequence of int
        ``(x, y)`` coordinates of the upper-left pixel where the insertion
        begins using 0-based indexing. Values may be negative or extend
        past the size of ``base_scene``; only the overlapping region is
        copied.

    Returns
    -------
    Scene
        New scene with photons from ``insert_scene`` written into the
        specified region of ``base_scene``.
    """

    if len(location) != 2:
        raise ValueError("location must have two elements (x, y)")

    if not np.array_equal(base_scene.wave, insert_scene.wave):
        raise ValueError("Scenes must share the same wavelength samples")

    x, y = [int(v) for v in location]

    base_photons = get_photons(base_scene).copy()
    insert_photons = get_photons(insert_scene)

    base_h, base_w = base_photons.shape[:2]
    ins_h, ins_w = insert_photons.shape[:2]

    # Determine overlap region in base scene coordinates
    x0 = max(x, 0)
    y0 = max(y, 0)
    x1 = min(x + ins_w, base_w)
    y1 = min(y + ins_h, base_h)

    if x0 >= x1 or y0 >= y1:
        # No overlap
        return Scene(photons=base_photons, wave=base_scene.wave, name=base_scene.name)

    # Corresponding region in insert scene coordinates
    src_x0 = x0 - x
    src_y0 = y0 - y
    src_x1 = src_x0 + (x1 - x0)
    src_y1 = src_y0 + (y1 - y0)

    base_photons[y0:y1, x0:x1, :] = insert_photons[src_y0:src_y1, src_x0:src_x1, :]

    return Scene(photons=base_photons, wave=base_scene.wave, name=base_scene.name)
