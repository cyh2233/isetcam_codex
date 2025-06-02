# mypy: ignore-errors
"""Display a Scene as an RGB image using Matplotlib."""

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


def scene_show_image(scene: Scene):
    """Render ``scene`` to sRGB and display with matplotlib.

    Parameters
    ----------
    scene : Scene
        Scene to visualise.

    Returns
    -------
    matplotlib.axes.Axes
        Axis containing the displayed image.
    """
    if plt is None:
        raise ImportError("matplotlib is required for scene_show_image")

    xyz = ie_xyz_from_photons(scene.photons, scene.wave)
    srgb, _, _ = xyz_to_srgb(xyz)
    img = np.clip(srgb, 0.0, 1.0)

    fig, ax = plt.subplots()
    ax.imshow(img)
    ax.axis("off")
    ie_format_figure(ax)
    return ax
