"""Plot camera sensor response and MTF curves."""

from __future__ import annotations

import numpy as np

try:
    import matplotlib.pyplot as plt
except Exception:  # pragma: no cover - matplotlib might not be installed
    plt = None  # type: ignore

from .camera_class import Camera
from .camera_mtf import camera_mtf
from ..sensor import sensor_plot


_DEF_TITLE_IMG = "Sensor response"
_DEF_TITLE_MTF = "MTF"


def camera_plot(camera: Camera, *, show_filters: bool = False,
                axes: "tuple[plt.Axes, plt.Axes] | None" = None) -> "tuple[plt.Axes, plt.Axes]":  # noqa: E501
    """Display sensor voltage image and MTF curve.

    Parameters
    ----------
    camera : Camera
        Camera instance to visualize.
    show_filters : bool, optional
        Overlay CFA letters on the sensor plot when ``True``.
    axes : tuple of matplotlib.axes.Axes, optional
        Tuple ``(ax_img, ax_mtf)`` used for plotting. If ``None`` new axes
        are created.

    Returns
    -------
    tuple[matplotlib.axes.Axes, matplotlib.axes.Axes]
        The axes used for the sensor image and MTF plot respectively.
    """
    if plt is None:
        raise ImportError("matplotlib is required for camera_plot")

    if axes is None:
        fig, (ax_img, ax_mtf) = plt.subplots(1, 2, figsize=(8, 4))
    else:
        ax_img, ax_mtf = axes
        fig = ax_img.figure

    sensor_plot(camera.sensor, show_filters=show_filters, ax=ax_img)
    ax_img.set_title(_DEF_TITLE_IMG)

    freqs, mtf = camera_mtf(camera)
    ax_mtf.plot(freqs, mtf)
    ax_mtf.set_xlabel("Spatial frequency (cycles/mm)")
    ax_mtf.set_ylabel("MTF")
    ax_mtf.set_title(_DEF_TITLE_MTF)
    ax_mtf.set_ylim(0.0, 1.05)

    fig.tight_layout()
    return ax_img, ax_mtf


__all__ = ["camera_plot"]
