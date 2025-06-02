# mypy: ignore-errors
"""Restrict a scene to a particular depth range."""

from __future__ import annotations

from typing import Sequence

import numpy as np

from .scene_class import Scene


def scene_depth_range(scene: Scene, depth_edges: Sequence[float]) -> tuple[Scene, np.ndarray]:
    """Mask photons outside ``depth_edges`` and return the depth-plane mask.

    Parameters
    ----------
    scene : Scene
        Scene containing a ``depth_map`` attribute.
    depth_edges : sequence of float
        ``(low, high)`` bounds of the desired depth range in meters.

    Returns
    -------
    (Scene, ndarray)
        Tuple of the new scene with masked photons and the boolean mask of
        pixels within the depth range.
    """
    dmap = getattr(scene, "depth_map", None)
    if dmap is None:
        raise AttributeError("scene must have a depth_map attribute")

    if len(depth_edges) != 2:
        raise ValueError("depth_edges must contain two values")
    low, high = float(depth_edges[0]), float(depth_edges[1])

    dmap = np.asarray(dmap)
    if dmap.ndim != 2:
        raise ValueError("scene.depth_map must be a 2-D array")

    d_plane = (low <= dmap) & (dmap < high)

    photons = np.asarray(scene.photons, dtype=float).copy()
    for i in range(photons.shape[2]):
        band = photons[:, :, i]
        band[~d_plane] = 0
        photons[:, :, i] = band

    out = Scene(photons=photons, wave=scene.wave, name=scene.name)
    out.depth_map = dmap * d_plane
    return out, d_plane


__all__ = ["scene_depth_range"]
