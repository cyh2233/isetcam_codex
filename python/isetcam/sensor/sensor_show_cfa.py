# mypy: ignore-errors
"""Visualize the color filter array pattern of a :class:`Sensor`."""

from __future__ import annotations

import numpy as np

try:  # pragma: no cover - matplotlib might not be installed
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
except Exception:  # pragma: no cover - matplotlib might not be installed
    plt = None  # type: ignore
    Rectangle = None  # type: ignore

from .sensor_class import Sensor
from ..ie_format_figure import ie_format_figure


_COLOR_MAP = {
    "r": (1.0, 0.0, 0.0),
    "g": (0.0, 1.0, 0.0),
    "b": (0.0, 0.0, 1.0),
    "c": (0.0, 1.0, 1.0),
    "m": (1.0, 0.0, 1.0),
    "y": (1.0, 1.0, 0.0),
    "k": (0.0, 0.0, 0.0),
    "w": (1.0, 1.0, 1.0),
}


def _parse_pattern(letters: np.ndarray | str) -> np.ndarray | None:
    """Return 2-D array of letters from ``letters`` if possible."""
    if isinstance(letters, str):
        size = int(np.sqrt(len(letters)))
        if size * size == len(letters):
            return np.array(list(letters)).reshape(size, size)
        return None
    letters = np.asarray(letters)
    if letters.ndim == 2:
        return letters
    if letters.ndim == 1:
        size = int(np.sqrt(letters.size))
        if size * size == letters.size:
            return letters.reshape(size, size)
    return None


def sensor_show_cfa(sensor: Sensor, ax: "plt.Axes | None" = None) -> "plt.Axes":
    """Plot the CFA color arrangement of ``sensor``.

    Parameters
    ----------
    sensor : Sensor
        Sensor instance containing the CFA description in the attribute
        ``filter_color_letters``.
    ax : matplotlib.axes.Axes, optional
        Axis used for plotting. When ``None`` a new axis is created.

    Returns
    -------
    matplotlib.axes.Axes
        The axis used for plotting.
    """

    if plt is None:
        raise ImportError("matplotlib is required for sensor_show_cfa")

    letters = getattr(sensor, "filter_color_letters", None)
    if letters is None:
        raise ValueError("sensor has no 'filter_color_letters' attribute")

    pattern = _parse_pattern(letters)
    if pattern is None:
        raise ValueError("filter_color_letters must form a square CFA pattern")

    rows, cols = pattern.shape

    if ax is None:
        _, ax = plt.subplots()

    for r in range(rows):
        for c in range(cols):
            ltr = str(pattern[r, c]).lower()
            color = _COLOR_MAP.get(ltr)
            if color is None:
                raise ValueError(f"Unknown CFA letter '{ltr}'")
            rect = Rectangle((c, r), 1, 1, facecolor=color, edgecolor="k")
            ax.add_patch(rect)

    ax.set_xlim(0, cols)
    ax.set_ylim(rows, 0)
    ax.set_aspect("equal")
    ax.axis("off")

    ie_format_figure(ax)
    return ax


__all__ = ["sensor_show_cfa"]
