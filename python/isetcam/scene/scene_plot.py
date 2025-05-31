"""Basic scene plotting utilities."""

from __future__ import annotations

import numpy as np

try:  # pragma: no cover - matplotlib might not be installed
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
except Exception:  # pragma: no cover - matplotlib might not be installed
    plt = None  # type: ignore
    Rectangle = None  # type: ignore

from .scene_class import Scene
from ..ie_xyz_from_photons import ie_xyz_from_photons
from ..srgb_xyz import xyz_to_srgb
from ..luminance_from_photons import luminance_from_photons
from ..ie_param_format import ie_param_format
from ..ie_format_figure import ie_format_figure


_DEF_KINDS = {
    "luminancehline",
    "luminancevline",
    "radiancehline",
    "radiancevline",
    "radianceimage",
    "radianceimagewithgrid",
}


def scene_plot(
    scene: Scene,
    kind: str = "luminancehline",
    loc: int | None = None,
    *,
    grid_spacing: int | None = None,
    roi: tuple[int, int, int, int] | None = None,
    ax: "plt.Axes | None" = None,
) -> "plt.Axes":
    """Plot various properties of ``scene``.

    Parameters
    ----------
    scene : Scene
        Scene to visualize.
    kind : str, optional
        One of ``'luminance hline'``, ``'luminance vline'``,
        ``'radiance hline'``, ``'radiance vline'``, ``'radiance image'`` or
        ``'radiance image with grid'``.
    loc : int, optional
        Row or column index for line plots. Defaults to the image center.
    grid_spacing : int, optional
        Overlay grid lines with this spacing in pixels when plotting the image.
    roi : tuple of int, optional
        ``(row, col, height, width)`` rectangle to overlay on the image.
    ax : matplotlib.axes.Axes, optional
        Axis to plot into. When ``None`` a new figure and axis are created.

    Returns
    -------
    matplotlib.axes.Axes
        Axis containing the plot.
    """
    if plt is None:
        raise ImportError("matplotlib is required for scene_plot")

    key = ie_param_format(kind)
    if key not in _DEF_KINDS:
        raise ValueError(f"Unknown plot kind '{kind}'")

    photons = np.asarray(scene.photons, dtype=float)
    wave = np.asarray(scene.wave, dtype=float).reshape(-1)
    rows, cols = photons.shape[:2]

    if key in {"luminancehline", "luminancevline"}:
        lum = luminance_from_photons(photons, wave)
        if key == "luminancehline":
            r = rows // 2 if loc is None else int(loc)
            profile = lum[r, :]
            pos = np.arange(cols)
            xlabel = "Column index"
        else:
            c = cols // 2 if loc is None else int(loc)
            profile = lum[:, c]
            pos = np.arange(rows)
            xlabel = "Row index"
        if ax is None:
            _, ax = plt.subplots()
        ax.plot(pos, profile, "k-")
        ie_format_figure(ax, xlabel=xlabel, ylabel="Luminance (cd/m$^2$)")
        return ax

    if key in {"radiancehline", "radiancevline"}:
        if key == "radiancehline":
            r = rows // 2 if loc is None else int(loc)
            data = photons[r, :, :]
            pos = np.arange(cols)
            xlabel = "Column index"
        else:
            c = cols // 2 if loc is None else int(loc)
            data = photons[:, c, :]
            pos = np.arange(rows)
            xlabel = "Row index"

        if data.ndim == 1:
            profile = data
        else:
            profile = data.mean(axis=1)
        if ax is None:
            _, ax = plt.subplots()
        ax.plot(pos, profile, "k-")
        ie_format_figure(ax, xlabel=xlabel, ylabel="Radiance (photons)")
        return ax

    # Image rendering
    xyz = ie_xyz_from_photons(photons, wave)
    srgb, _, _ = xyz_to_srgb(xyz)
    img = np.clip(srgb, 0.0, 1.0)
    if ax is None:
        _, ax = plt.subplots()
    ax.imshow(img)
    ax.axis("off")

    if grid_spacing is not None:
        g = int(grid_spacing)
        for r in range(0, rows, g):
            ax.axhline(r - 0.5, color="k", linewidth=0.5)
        for c in range(0, cols, g):
            ax.axvline(c - 0.5, color="k", linewidth=0.5)
    if roi is not None and Rectangle is not None:
        r0, c0, h, w = [int(v) for v in roi]
        rect = Rectangle((c0, r0), w, h, edgecolor="y", facecolor="none", linewidth=1)
        ax.add_patch(rect)

    ie_format_figure(ax)
    return ax


__all__ = ["scene_plot"]
