# mypy: ignore-errors
"""Overlay depth map contours on a Scene RGB image."""

from __future__ import annotations

import numpy as np

try:  # pragma: no cover - matplotlib might not be installed
    import matplotlib.pyplot as plt
except Exception:  # pragma: no cover - matplotlib might not be installed
    plt = None  # type: ignore

from .scene_class import Scene
from ..ie_xyz_from_photons import ie_xyz_from_photons
from ..srgb_xyz import xyz_to_srgb
from ..ie_format_figure import ie_format_figure


def scene_depth_overlay(scene: Scene, n: int = 10):
    """Display the scene RGB image with depth map contours overlaid.

    Parameters
    ----------
    scene : Scene
        Scene containing a ``depth_map`` attribute.
    n : int, optional
        Number of contour levels. Default is 10.

    Returns
    -------
    matplotlib.axes.Axes
        Axis containing the displayed image and contour overlay.
    """
    if plt is None:
        raise ImportError("matplotlib is required for scene_depth_overlay")

    dmap = getattr(scene, "depth_map", None)
    if dmap is None:
        raise AttributeError("scene must have a depth_map attribute")
    dmap = np.asarray(dmap)
    if dmap.ndim != 2:
        raise ValueError("scene.depth_map must be a 2-D array")

    xyz = ie_xyz_from_photons(scene.photons, scene.wave)
    srgb, _, _ = xyz_to_srgb(xyz)
    img = np.clip(srgb, 0.0, 1.0)

    fig, ax = plt.subplots()
    ax.imshow(img)
    levels = np.linspace(dmap.min(), dmap.max(), n)
    ax.contour(dmap, levels=levels, colors="k", linewidths=1)
    ax.axis("off")
    ie_format_figure(ax)
    return ax


__all__ = ["scene_depth_overlay"]
