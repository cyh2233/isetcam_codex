"""Combine two scenes horizontally, vertically, or in a grid."""

from __future__ import annotations

import numpy as np

from .scene_class import Scene


_VALID_DIRS = {"horizontal", "vertical", "both", "centered"}


def scene_combine(scene1: Scene, scene2: Scene, direction: str = "horizontal") -> Scene:
    """Combine two scenes using the specified orientation.

    Parameters
    ----------
    scene1 : Scene
        First scene to combine.
    scene2 : Scene
        Second scene to combine. Must have the same wavelength sampling as
        ``scene1``.
    direction : {"horizontal", "vertical", "both", "centered"}, optional
        Orientation of the combination. Defaults to ``"horizontal"``.

    Returns
    -------
    Scene
        New scene containing the combined photon data with the same wavelength
        samples.
    """

    if direction is None:
        direction = "horizontal"
    direction = str(direction).lower()
    if direction not in _VALID_DIRS:
        raise ValueError("direction must be 'horizontal', 'vertical', 'both', or 'centered'")  # noqa: E501

    if not np.array_equal(scene1.wave, scene2.wave):
        raise ValueError("Scenes must have matching wavelength samples")

    p1 = scene1.photons
    p2 = scene2.photons
    r1, c1 = p1.shape[:2]
    r2, c2 = p2.shape[:2]

    if direction == "horizontal":
        if r1 != r2:
            raise ValueError("Scenes must have the same number of rows for horizontal combination")  # noqa: E501
        photons = np.concatenate((p1, p2), axis=1)
        return Scene(photons=photons, wave=scene1.wave, name=scene1.name)

    if direction == "vertical":
        if c1 != c2:
            raise ValueError("Scenes must have the same number of columns for vertical combination")  # noqa: E501
        photons = np.concatenate((p1, p2), axis=0)
        return Scene(photons=photons, wave=scene1.wave, name=scene1.name)

    if direction == "both":
        tmp = scene_combine(scene1, scene2, "horizontal")
        return scene_combine(tmp, tmp, "vertical")

    # centered
    mid = scene_combine(scene1, scene2, "horizontal")
    mid = scene_combine(scene2, mid, "horizontal")
    edge = scene_combine(scene2, scene2, "horizontal")
    edge = scene_combine(edge, scene2, "horizontal")
    tmp = scene_combine(edge, mid, "vertical")
    return scene_combine(tmp, edge, "vertical")

