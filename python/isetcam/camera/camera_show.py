# mypy: ignore-errors
"""Display parts of a :class:`Camera` using Matplotlib."""

from __future__ import annotations

import numpy as np

try:  # pragma: no cover - matplotlib might not be installed
    import matplotlib.pyplot as plt
except Exception:  # pragma: no cover - matplotlib might not be installed
    plt = None  # type: ignore

from .camera_class import Camera
from ..ie_format_figure import ie_format_figure
from ..opticalimage import oi_show_image
from ..sensor import sensor_show_image


_DEF_KINDS = {"oi", "sensor", "ip"}


def camera_show(camera: Camera, which: str = "ip"):
    """Display ``camera`` data using matplotlib.

    Parameters
    ----------
    camera : Camera
        Camera instance whose data should be visualized.
    which : str, optional
        One of ``"oi"``, ``"sensor"`` or ``"ip"`` indicating what to show.
        Defaults to ``"ip"``.

    Returns
    -------
    matplotlib.axes.Axes
        Axis with the displayed image.
    """
    if plt is None:
        raise ImportError("matplotlib is required for camera_show")

    key = str(which).lower().replace(" ", "")
    if key not in _DEF_KINDS:
        raise ValueError(f"Unknown show option '{which}'")

    if key == "oi":
        return oi_show_image(camera.optical_image)

    if key == "sensor":
        return sensor_show_image(camera.sensor)

    # key == "ip"
    if not hasattr(camera, "ip"):
        raise ValueError("Camera has no 'ip' attribute")
    img = np.asarray(camera.ip.rgb, dtype=float)
    if img.ndim != 3 or img.shape[2] != 3:
        raise ValueError("camera.ip.rgb must be (rows, cols, 3)")

    fig, ax = plt.subplots()
    ax.imshow(np.clip(img, 0.0, 1.0))
    ax.axis("off")
    ie_format_figure(ax)
    return ax


__all__ = ["camera_show"]
